window.addEventListener('load', () => {

	var item = document.querySelector("#employee_id");
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

		let data = {'employee_id': item[0]};

		fetch("/login", {
		  method: "POST", 
		  body: JSON.stringify(data)
		});
	}

});