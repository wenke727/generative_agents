## 前后端交互

###

```javascript
		// console.log("phase: " + phase + ", step: " + step);
		// *** MOVE PERSONAS ***
		// Moving personas take place in three distinct phases: "process," "update,"
		// and "execute." These phases are determined by the value of <phase>.
		// Only one of the three phases is incurred in each update cycle.
		if (phase == "process") {
			// "process" takes all current locations of the personas and send them to
			// the frontend server in a json form. Here, we first create the json
			// file that records all persona locations:
			let data = {
				"step": step,
				"sim_code": sim_code,
				"environment": {}
			}
			for (let i = 0; i < Object.keys(personas).length; i++) {
				let persona_name = Object.keys(personas)[i];
				data["environment"][persona_name] = {
					"maze": curr_maze,
					"x": Math.ceil((personas[persona_name].body.position.x) / tile_width),
					"y": Math.ceil((personas[persona_name].body.position.y) / tile_width)
				}
			}
			var json = JSON.stringify(data);
			// We then send this to the frontend server:
			var retrieve_xobj = new XMLHttpRequest();
			retrieve_xobj.overrideMimeType("application/json");
			retrieve_xobj.open('POST', "{% url 'process_environment' %}", true);
			retrieve_xobj.send(json);
			// Finally, we update the phase variable to start the "udpate" process.
			// Now that we sent all persona locations to the backend server, we need
			// to wait until the backend determines what the personas will do next.
			phase = "update";
		}
```


###

```javascript
	  else if (phase == "update") {
		  // Update is where we * wait * for the backend server to finish
		  // computing about what the personas will do next given their current
		  // situation.
		  // We do this by continuously asking the backend server if it is ready.
		  // The backend server is ready when it returns a json that has a key-val
		  // pair with "<move>": true.
		  // Note that we do not want to overburden the backend too much by
		  // over-querying; so, we have a timer set so we only query it once every
		  // timer_max cycles.
		  if (timer <= 0) {
			  var update_xobj = new XMLHttpRequest();
			  update_xobj.overrideMimeType("application/json");
			  update_xobj.open('POST', "{% url 'update_environment' %}", true);
			  update_xobj.addEventListener("load", function () {
				  if (this.readyState === 4) {
					  if (update_xobj.status === 200) {
						  if (JSON.parse(update_xobj.responseText)["<step>"] == step) {
							  execute_movement = JSON.parse(update_xobj.responseText)
							  phase = "execute";
						  }
						  timer = timer_max;
					  }
				  }
			  });
			  update_xobj.send(JSON.stringify({ "step": step, "sim_code": sim_code }));
		  }
		  timer = timer - 1;
	  }

```