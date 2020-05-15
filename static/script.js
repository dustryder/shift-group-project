//Datatable functionality
$(document).ready(function(){
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#DeviceTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});


window.addEventListener('load', () => {

	var item = document.querySelector("#employee_id");
	var status = document.querySelectorAll("[hidden-employee-id]");
	item.addEventListener('change', employeeChange);

	function employeeChange() {
		var item = document.querySelector("#employee_id");
		item = item.value.split(",");
		var admin = document.querySelector("a[href*='admin']");
		let employee_permission = item[2];
		if (employee_permission >= 10) {

			admin.innerText="Admin";
		} else {
			admin.innerText="";
		}

		let employeeId = item[0];

		for (var i = 0; i < status.length; i++ ) {

			if (employeeId == status[i].getAttribute('hidden-employee-id')) {

				let startDate = status[i].getAttribute('hidden-date');
				let deviceId = status[i].parentNode.getAttribute('hidden-device-id');

				status[i].innerHTML = `<button class="btn btn-primary btn-block" type="submit" name="device_id" value=${deviceId + "," + item[1] + ',' + startDate}>Return</button>`
			} else {
				status[i].innerHTML = status[i].getAttribute('hidden-name');
			}
		}


		let data = {'employee_id': item[0]};

		fetch("/login", {
		  method: "POST", 
		  body: JSON.stringify(data)
		});

		if (employee_permission >= 5) {

			for (var i = 0; i < overdue_devices.length; i++) {
				let item = document.querySelector(`[hidden-device-id='${overdue_devices[i]}']`);
				item.classList.add('table-danger');
			}

		} else {
			let items = document.querySelectorAll("tr");
			for (var i = 0; i < items.length; i++) {
				items[i].classList.remove('table-danger');
			}
		}

	}

	//Populates device history and info modal form
	let tableRows = document.querySelectorAll('[hidden-device-id]');
	tableRows.forEach(row => {
		row.addEventListener('click', (event) => {
			if (event.target.tagName !== "BUTTON") {

				var modalData;

				let device_id = row.getAttribute('hidden-device-id');
				let data = {'device_id': device_id};

				fetch("/device-history", {
				  method: "POST", 
				  body: JSON.stringify(data)
				}).then(response => response.json())
				.then(data => {
					let historyData = data[0];
					let deviceData = data[1][0];
					let employee_permission = item.value.split(",")[2];

					let deviceInformation = document.querySelector("#deviceInformationBody");
					let deviceInformationTitles = ['Device Name', 'Device Type', 'OS Type', 'OS Version', 'RAM', 'CPU', 'Bit', 'Resolution', 'Grade', 'UUID', 'Acquisition Date'];
					deviceInformation.innerHTML = "";

					//Render the device info body
					for(var i = 0; i < deviceData.length - 1; i++) {

						var newListItem = document.createElement("li");

						if (deviceInformationTitles[i] === 'Acquisition Date') {
							let date = moment(deviceData[i]);
							var newText = document.createTextNode(`${deviceInformationTitles[i]}: ${date.format('DD/MM/YYYY')}`);

						} else {
							let field = deviceData[i];
							if (!field) field = 'Unknown';
							var newText = document.createTextNode(`${deviceInformationTitles[i]}: ${field}`);
						}


						newListItem.appendChild(newText);
						deviceInformation.appendChild(newListItem);
					}

					var newListItem = document.createElement("li");

					if (employee_permission == 1) {

						let field = deviceData[deviceData.length - 1];
						if (field) {
							var newText = document.createTextNode(`Loan End: ${moment(field).format('DD/MM/YYYY')}`);
							newListItem.appendChild(newText);
							deviceInformation.appendChild(newListItem);
						}

					}

					let tableBody = document.querySelector("#historyTableBody");
					let tableContainer = document.querySelector("#historyTableContainer");
					tableBody.innerHTML = "";

					//Render the device history body
					if (employee_permission >= 5) {

						tableContainer.classList.remove("d-none");

						for(var i = 0; i < historyData.length; i++) {

							let newRow = tableBody.insertRow();

							for(var j = 0; j < historyData[i].length; j++) {

								let newCell = newRow.insertCell(j);
								if (j > 1) {
									let date = moment(historyData[i][j]).format('DD/MM/YYYY')
									if (date == 'Invalid date') date = 'On Loan';
									var newText = document.createTextNode(date);
								} else {
									var newText = document.createTextNode(historyData[i][j]);
								}

								newCell.appendChild(newText);
							}
						}

					} else {
						tableContainer.classList.add("d-none");
					}




				});


				$('#deviceInfoModal').modal('show');
			}
		});
	});


	//Populates device loan modal form with device information and hidden identifiers
	var submitButtons = document.querySelectorAll("button[data-target='#bookingModal']");
	submitButtons.forEach(button => {
		button.addEventListener('click', () => {



			let data = button.value.split(',');
			let employee_id = item.value.split(",")[0];
			data.push(employee_id);
			
			let formItems = document.querySelectorAll("form[action='/loan-device'] input");
			for(var i = 0; i < data.length; i++) {

				let currentNode = formItems[i];

				if (data[i] != "None") {
					currentNode.value = data[i];
				} else {
					currentNode.value = "Unknown";
				}
			}

		});
	});

});