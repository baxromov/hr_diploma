var chart = function () {
  var chart = document.getElementsByClassName('chart')[0];
  var divs = chart.getElementsByTagName('div');
  var buttons = document.getElementsByClassName('btn-bar');

  function init() {
    showExpense();
  }

  function showExpense() {
    for (var i = 0; i < divs.length; i++) {
      divs[i].style.height = divs[i].dataset.earnings * 2 + 'px';
    }
    activeButton(0);
    chart.classList.remove('expense');
  }

  function showEarnings() {
    for (var i = 0; i < divs.length; i++) {
      divs[i].style.height = divs[i].dataset.expense * 4 + 'px';
    }
    activeButton(1);
    chart.classList.add('expense');
  }

  function activeButton(active) {
    if (active === 0) {
      buttons[0].classList.add('active');
      buttons[1].classList.remove('active');
    } else {
      buttons[1].classList.add('active');
      buttons[0].classList.remove('active');
    }
  }

  buttons[0].addEventListener('click', showExpense);
  buttons[1].addEventListener('click', showEarnings);

  return { init: init };
}();

document.addEventListener('DOMContentLoaded', chart.init);