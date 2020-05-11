window.addEventListener('load', () => {

	var item = document.querySelector("#employee_id");
	item.addEventListener('change', employeeChange);

	function employeeChange() {
		var item = document.querySelector("#employee_id");
		let data = {'employee_id': item.value};
		fetch("/", {
		  method: "POST", 
		  body: JSON.stringify(data)
		}).then(() => {;
		location.reload(true);
		});
	}

});