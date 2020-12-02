function roll() {
  var num = document.getElementById("number").value; 
  var sides = document.getElementById("sides").value;
  var result = 0;
  
  for (i = 0; i < num; i++) {
    result += Math.floor(Math.random() * sides) + 1;
  }
  
  document.getElementById("placeholder").innerHTML = result;
}               