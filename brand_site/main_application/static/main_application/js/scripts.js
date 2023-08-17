// СКРИПТ ВЫПАДАЮЩЕГО МЕНЮ

const menu = document.querySelector("#mouse-menu");
const dropDownMenu = document.getElementById("drop-down");
const body = document.getElementsByTagName("body")[0];

menu.addEventListener('mouseover', () => {
    dropDownMenu.style.display = "block";
    dropDownMenu.style.zIndex = "1";
    dropDownMenu.style.backgroundColor = "#fafafa";
});

dropDownMenu.addEventListener('mouseleave', () => {
    dropDownMenu.style.display = "none";
});

menu.addEventListener('mouseleave', () => {
    dropDownMenu.style.display = "none";
});


  