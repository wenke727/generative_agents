#%%
import sys
sys.path.append('../')
from dotenv import load_dotenv
load_dotenv('../.env')

import os
import json
import pandas as pd
from loguru import logger

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance


def get_qdrant_client_cfg():
    """读取并解析 QDRANT_CLIENT_CFG"""
    qdrant_client_cfg = json.loads(
        os.environ.get(
            "QDRANT_CLIENT_CFG",
            '{"location": ":memory:"}'
        )
    )

    return qdrant_client_cfg

class VectoreDB:
    def __init__(self, cfg, collection_name, embed_dim):
        self.client = QdrantClient(**cfg)
        self.collection_name = collection_name

        self.create_collection(
            collection_name = self.collection_name,
            vectors_config = VectorParams(size=embed_dim, distance=Distance.COSINE),
        )

    def create_collection(self, collection_name, vectors_config):
        """
        Create a collection in Qdrant if it does not exist.
        """
        if self.client.collection_exists(self.collection_name):
            return False

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config
        )
        return True

    def add(self, points):
        """
        Add or upsert points into the collection.

        :param points: A list of PointStruct to be added.
        :return: Operation info from Qdrant.
        """
        return self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True
        )

    def delete(self, point_ids):
        """
        Delete points from the collection by their IDs.

        :param point_ids: A list of point IDs to delete.
        :return: Operation info from Qdrant.
        """
        # First, retrieve the points to check if they exist
        existing_points = self.client.retrieve(collection_name=self.collection_name, ids=point_ids)

        if not existing_points:
            logger.warning("No points found with the provided IDs, nothing to delete.")
            return {"status": "No points found with the provided IDs, nothing to delete."}

        # If points exist, proceed with deletion
        return self.client.delete(
            collection_name=self.collection_name,
            points_selector=point_ids
        )

    def modify(self, uuid, *args, **kwargs):
        """
        Modify the payload of a vector in the collection.

        :param uuid: The ID of the vector to modify.
        :param args: List of key-value pairs to update in the payload.
        :param kwargs: Dictionary of key-value pairs to update in the payload.
        :return: The updated payload.
        """
        existing_points = self.client.retrieve(collection_name=self.collection_name, ids=[uuid])

        if not existing_points:
            raise ValueError(f"No vector found with ID {uuid} in collection {self.collection_name}.")

        existing_payload = existing_points[0].payload

        for key, value in args:
            existing_payload[key] = value

        existing_payload.update(kwargs)

        self.client.set_payload(
            collection_name=self.collection_name,
            payload=existing_payload,
            points=[uuid]
        )

        return existing_payload

    def search(self, query_vector, to_df=True, limit=128):
        """
        Query the collection using a vector.

        :param query_vector: The vector to search for.
        :param limit: The maximum number of results to return.
        :return: A list of search results.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit
        )

        if to_df:
            res = pd.DataFrame([
                {'id': i.id, **i.payload, 'score': i.score}
                    for i in search_result]
            )

            return res

        # payloads = [hit.payload for hit in search_result]
        return search_result

    def search_with_filter(self, query_vector, filter_condition, limit=10):
        """
        Search the collection using a vector with a filter condition.

        :param query_vector: The vector to search for.
        :param filter_condition: The condition to filter search results.
        :param limit: The maximum number of results to return.
        :return: A list of search results.
        """
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            filter=filter_condition
        )
        return [hit.payload for hit in search_result]

    def get_collection_info(self):
        """
        Get information about the collection.

        :return: A dictionary with collection information.
        """
        return self.client.get_collection(self.collection_name)

    def clear_collection(self):
        """
        Remove all points from the collection.

        :return: Operation info from Qdrant.
        """
        return self.client.clear_payload(collection_name=self.collection_name)

    def delete_collection(self):
        """
        Delete the entire collection and its contents.

        :return: Operation info from Qdrant.
        """
        return self.client.delete_collection(self.collection_name)

    def retrieve_points(self, point_ids):
        """
        Retrieve multiple points by their IDs.

        :param point_ids: A list of point IDs to retrieve.
        :return: A list of points with their details.
        """
        return self.client.retrieve(collection_name=self.collection_name, ids=point_ids)

    def search_recent_with_filters(self, query_vector, limit=10, filters=None):
        """
        Search the collection for the most recent points with additional filtering.

        :param query_vector: The vector to search for.
        :param limit: The maximum number of results to return (default is 10).
        :param filters: A dictionary of filtering conditions. Example:
                        {"must": [{"key": "some_attribute", "match": {"value": "some_value"}}]}
        :return: A list of search results, sorted by the most recent timestamp.
        """
        # Define the filtering condition
        filter_condition = filters if filters else {}

        # Define the sorting condition by timestamp in descending order (most recent first)
        sort_by_timestamp = [
            {"key": "timestamp", "order": "desc"}  # Sort by timestamp in descending order
        ]

        # Perform the search with filter and sorting
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            filter=filter_condition,
            with_payload=True,  # Ensure we retrieve payload data (which includes timestamp)
            sort=sort_by_timestamp
        )

        # Extract and return the payloads of the search results
        return [hit.payload for hit in search_result]

    def get_recent_records(self, limit=10, filters=None):
        """
        Retrieve the most recent records from the collection based on timestamp, with additional filtering.

        :param limit: The maximum number of results to return (default is 10).
        :param filters: A dictionary of filtering conditions. Example:
                        {"must": [{"key": "some_attribute", "match": {"value": "some_value"}}]}
        :return: A list of the most recent records, sorted by the most recent timestamp.
        """
        # Define the filtering condition
        filter_condition = filters if filters else {}

        # Define the sorting condition by timestamp in descending order (most recent first)
        sort_by_timestamp = [
            {"key": "timestamp", "order": "desc"}  # Sort by timestamp in descending order
        ]

        # Perform the search with filter and sorting, without using any query vector
        search_result = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            filter=filter_condition,
            with_payload=True,  # Ensure we retrieve payload data (which includes timestamp)
            sort=sort_by_timestamp
        )

        # Extract and return the payloads of the search results
        return [hit.payload for hit in search_result]


if __name__ == "__main__":
    # client_cfg = {'path': "./db"}
    client_cfg = get_qdrant_client_cfg()
    collection_name = "demo_collection"

    client = VectoreDB(client_cfg, collection_name, 4)

    points = [
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ]

    # insert
    client.add(points)

    # delete
    client.delete([4])
    client.delete([4])

    # delete
    client.modify(uuid=3, city='深圳')

    # search
    res = client.search(query_vector=[0.2, 0.1, 0.9, 0.7], limit=6)
    res
    # pd.DataFrame(res)

    # from persona.prompt_template.openai_helper import initialize_openai_client
    # client, chat, embeddings = initialize_openai_client()


