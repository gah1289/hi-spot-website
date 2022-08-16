const cancelEvtModal = document.getElementById('cancelEvtModal');
const myInput = document.getElementById('myInput');
const deleteEvtModal = document.getElementById('deleteEvtModal');

cancelEvtModal.addEventListener('shown.bs.modal', () => {
	myInput.focus();
});

deleteEvtModal.addEventListener('shown.bs.modal', () => {
	myInput.focus();
});
