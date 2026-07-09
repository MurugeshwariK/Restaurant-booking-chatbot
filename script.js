<!DOCTYPE html>
<html>
<head>

<title>TableBot</title>
<link rel="stylesheet" href="style.css">

</head>
<body>


<div class="container">


<!-- SIDEBAR -->

<div class="sidebar">

<h1>TableBot</h1>

<p>Restaurant Booking Assistant</p>


<button onclick="quick('show restaurants')">
🍽 Find Restaurants
</button>

<button onclick="quick('book table')">
📅 Book a Table
</button>

<button onclick="quick('check availability')">
✅ Check Availability
</button>

<button onclick="quick('modify booking')">
✏️ Modify Booking
</button>

<button onclick="quick('cancel booking')">
❌ Cancel Booking
</button>


</div>



<!-- CHAT -->

<div class="chat">

<h2>TableBot</h2>


<div id="box">

<div class="bot">Welcome to TableBot! 🍽

I can help you with:

🍽  Show Restaurants
📅 Book a Table
✅ Check Availability
✏️  Modify Booking
❌ Cancel Booking

Click a button on the left or type your message below!</div>

</div>


<div class="input-area">

<input
id="msg"
placeholder="Type your message..."
onkeydown="if(event.key==='Enter') send()"
>

<button onclick="send()">
Send
</button>

</div>


</div>


</div>


<script src="script.js"></script>

</body>
</html>