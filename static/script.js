window.addEventListener('load', () => {

	var item = document.querySelector("#employee_id");
	var status = document.querySelectorAll("[hidden-id]");
	item.addEventListener('change', employeeChange);

	function employeeChange() {
		var item = document.querySelector("#employee_id");
		item = item.value.split(",");
		var admin = document.querySelector("a[href*='admin']");
		if (item[2] >= 10) {

			admin.innerText="Admin";
		} else {
			admin.innerText="";
		}

		let employeeId = item[0];

		for (var i = 0; i < status.length; i++ ) {


			if (employeeId === status[i].getAttribute('hidden-id')) {
				status[i].innerHTML = `<button class="btn btn-primary btn-block" type="submit" name="device_id" value=${employeeId + "," + item[1]}>Return</button>`
			} else {
				status[i].innerHTML = status[i].getAttribute('hidden-name');
			}
		}


		let data = {'employee_id': item[0]};

		fetch("/login", {
		  method: "POST", 
		  body: JSON.stringify(data)
		});
	}

});