import os
from loguru import logger
from typing import Dict, List, Optional, Union
from pymilvus import MilvusClient, DataType

COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "memory")
EMBEDDING_DIM = os.environ.get("EMBEDDING_DIM", 1536)
MILVUS_URI = os.environ.get("MILVUS_URI", "../data/test_milvus.db")


class VectorDB:
    def __init__(self, collection_name, embedding_dim, milvus_uri=MILVUS_URI):
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self.milvus_uri = milvus_uri or os.environ.get("MILVUS_URI", "../data/test_milvus.db")
        self.client = MilvusClient(self.milvus_uri)

        self.schema = None
        self.index_params = None

    def create_schema(self):
        """Creates a schema for the collection."""
        schema = self.client.create_schema(enable_dynamic_field=True)
        schema.add_field(field_name='id', datatype=DataType.INT64, is_primary=True, auto_id=False)
        schema.add_field(field_name='owner', datatype=DataType.VARCHAR, max_length=100)
        schema.add_field(field_name='subject', datatype=DataType.VARCHAR, max_length=100)
        schema.add_field(field_name='predicate', datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name='object', datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name='created', datatype=DataType.VARCHAR, max_length=50)
        schema.add_field(field_name='embedding_key', datatype=DataType.VARCHAR, max_length=4096)
        schema.add_field(field_name='poignancy', datatype=DataType.INT64)
        schema.add_field(field_name='vector', datatype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)
        self.schema = schema

        formatted_json = str(schema.fields).replace('}, {', '}, \n {')
        logger.debug(f"schema:\n{formatted_json}")
        return schema

    def create_index_params(self):
        """Creates index parameters for the collection."""
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name='vector',
            # index_type="IVF_FLAT",
            metric_type='IP',
            index_name="text_emb",
            params={"nlist": 128}
        )
        index_params.add_index(field_name='subject', index_name='subject_index')
        index_params.add_index(field_name='predicate', index_name='predicate_index')
        index_params.add_index(field_name='object', index_name='object_index')

        self.index_params = index_params
        formatted_json = str(index_params).replace('}, {', '}, \n {')
        logger.debug(f"index_params: \n{formatted_json}")

        return index_params

    def create_collection(self, replace=False):
        """Drops and creates the collection with schema and index."""
        if self.client.has_collection(self.collection_name):
            if not replace:
                self.client.load_collection(self.collection_name)
                return
            self.client.drop_collection(self.collection_name)

        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=self.embedding_dim,
            schema=self.schema,
            index_params=self.index_params
        )
        indexes = self.client.list_indexes(self.collection_name)
        logger.debug(f"Indexes: {indexes}")

        return

    def insert(self, all_points, **kwargs):
        """Inserts data into the collection."""
        self.client.insert(self.collection_name, all_points, **kwargs)

    def delete(self, **kwargs):
        return self.client.delete(self.collection_name, **kwargs)

    def delete_by_ids(self, ids:list, **kwargs):
        return self.client.delete(self.collection_name, ids, **kwargs)

    """ search, query & get """
    def search(
        self,
        data: Union[List[list], list],
        filter: str = "",
        limit: int = 10,
        output_fields: Optional[List[str]] = None,
        search_params: Optional[dict] = None,
        timeout: Optional[float] = None,
        partition_names: Optional[List[str]] = None,
        anns_field: Optional[str] = None,
        **kwargs,
    ):
        return self.client.search(
            self.collection_name,
            data=data,
            filter=filter,
            limit=limit,
            output_fields=output_fields,
            search_params=search_params,
            timeout=timeout,
            partition_names=partition_names,
            anns_field=anns_field,
            **kwargs
        )

    def get(self, ids, output_fields=None, timeout=None, partition_names=None, **kwargs):
        """
        Grab the inserted vectors using the primary key from the Collection.
        """
        return self.client.get(
            self.collection_name,
            ids=ids,
            output_fields=output_fields,
            timeout=timeout,
            partition_names=partition_names,
            **kwargs
        )

    def query(
        self,
        filter: str = "",
        output_fields: Optional[List[str]] = None,
        timeout: Optional[float] = None,
        ids: Optional[Union[List, str, int]] = None,
        partition_names: Optional[List[str]] = None,
        **kwargs,
    ):
        return self.client.query(
            self.collection_name,
            filter=filter,
            output_fields=output_fields,
            timeout=timeout,
            ids=ids,
            partition_names=partition_names,
            **kwargs
        )

    def update(self, ids, update_params: dict, timeout=None, partition_names=None, **kwargs):
        data = self.get(ids=ids)
        for i in data:
            for key, val in update_params.items():
                i[key] = val

        return self.client.upsert(
            self.collection_name,
            data=data,
            timeout=timeout,
            partition_name=partition_names,
            **kwargs
        )

    def get_collection_stats(self):
        """Retrieves collection statistics."""
        return self.client.get_collection_stats(self.collection_name)


if __name__ == "__main__":
    vector_db = VectorDB(COLLECTION_NAME, EMBEDDING_DIM)

    vector_db.create_collection(replace=False)
    client = vector_db.client

    # 增
    # vector_db.insert(COLLECTION_NAME, all_points)

    # 删
    # vector_db.delete(filter="")
    # vector_db.delete_by_ids(ids=[1,2])

    # 改
    # vector_db.update([1], {'node_count': -1})

    # 查
    # vector_db.get(ids=[1, 2])
    # vector_db.query(filter=' id in [1, 2] ')
    # vector_db.searc(xxx)

    # 获取状态
    client.get_collection_stats(COLLECTION_NAME)

