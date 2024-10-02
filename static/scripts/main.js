window.onload = function() {
	const scrollContainer = document.getElementById('table-container');
	
	// Прокрутка вниз
	scrollContainer.scrollTo({
		top: 300, // Сколько пикселей прокрутить вниз
		behavior: 'smooth' // Плавная прокрутка
	});

	// Вернуться обратно через 1 секунду
	setTimeout(() => {
		scrollContainer.scrollTo({
			top: 0, // Вернуться в начало
			behavior: 'smooth' // Плавная прокрутка
		});
	}, 1000); // Время задержки перед возвратом
};

const copyPcCode = document.getElementById('copyPcCode');

copyPcCode.addEventListener('click', function() {
	var pcCode = copyPcCode.getAttribute("code");
	navigator.clipboard.writeText(pcCode).then(() => {
		alert('Код скопирован в буфер обмена!');
	}).catch(err => {
		console.error('Ошибка при копировании текста: ', err);
	});
})

const rows = document.querySelectorAll('.task-container tr');
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modalTitle');
const modalCommand = document.getElementById('modalCommand');
const modalResponse = document.getElementById('modalResponse');
const closeBtn = document.getElementById('close');

// Устанавливаем обработчик для каждой строки таблицы
rows.forEach(row => {
	if (row.id != "tableHeaders") {
		var tds = row.querySelectorAll('td');
		console.log(tds);
		row.addEventListener('click', () => {
			modalTitle.innerText = `Command #${tds[0].textContent}\n${tds[5].textContent} `;
			if (tds[1].textContent == "")
				tds[1].textContent = "..."
			if (tds[7].textContent == "")
				tds[7].textContent = "no response"
			modalCommand.innerHTML = `<span style="color: rgb(21,171,13)">${tds[2].textContent}@RemoteSH</span>:<span style="color: rgb(29,88,255)">~/</span>$ ${tds[1].textContent}`;
			modalResponse.innerText = `${tds[7].textContent}`;
			
			modal.style.display = 'flex';
		});
	}
});

// Закрываем модальное окно при нажатии на кнопку закрытия
closeBtn.addEventListener('click', () => {
	modal.style.display = 'none';
});

// Закрываем окно при клике вне его
window.addEventListener('click', (event) => {
	if (event.target === modal) {
		modal.style.display = 'none';
	}
});