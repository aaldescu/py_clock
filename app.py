import json
import sqlite3
from sqlite3 import Error
from datetime import datetime

def hello(environ, start_response):
	
	conn = None
	try:
		conn = sqlite3.connect('ovkino.db')
	except Error as e:
		print(e)


	cur = conn.cursor()
	cur.execute("SELECT DISTINCT kino,movie,hour,day from PLAYTIME")

	rows = cur.fetchall()

	events = []
	for row in rows:
		event_dict = {}
		event_dict = {'title' : row[1] ,'description' : 'Playing at ' + row[0] , 'start':row[3]+'T'+row[2] }
		events.append(event_dict)
		

	events_string = json.dumps(events, indent = 4, sort_keys=True)

	now = datetime.now()
	today = now.strftime("%Y-%m-%d")
        
	html_text = """
<html>

<head>
<meta charset='utf-8' />

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

#calendar {
  max-width: 900px;
  margin: 40px auto;
}

</style>

<style>

  /*
  i wish this required CSS was better documented :(
  https://github.com/FezVrasta/popper.js/issues/674
  derived from this CSS on this page: https://popper.js.org/tooltip-examples.html
  */

  .popper,
  .tooltip {
	position: absolute;
	z-index: 9999;
	background: #FFC107;
	color: black;
	width: 150px;
	border-radius: 3px;
	box-shadow: 0 0 2px rgba(0,0,0,0.5);
	padding: 10px;
	text-align: center;
  }
  .style5 .tooltip {
	background: #1E252B;
	color: #FFFFFF;
	max-width: 200px;
	width: auto;
	font-size: .8rem;
	padding: .5em 1em;
  }
  .popper .popper__arrow,
  .tooltip .tooltip-arrow {
	width: 0;
	height: 0;
	border-style: solid;
	position: absolute;
	margin: 5px;
  }

  .tooltip .tooltip-arrow,
  .popper .popper__arrow {
	border-color: #FFC107;
  }
  .style5 .tooltip .tooltip-arrow {
	border-color: #1E252B;
  }
  .popper[x-placement^="top"],
  .tooltip[x-placement^="top"] {
	margin-bottom: 5px;
  }
  .popper[x-placement^="top"] .popper__arrow,
  .tooltip[x-placement^="top"] .tooltip-arrow {
	border-width: 5px 5px 0 5px;
	border-left-color: transparent;
	border-right-color: transparent;
	border-bottom-color: transparent;
	bottom: -5px;
	left: calc(50% - 5px);
	margin-top: 0;
	margin-bottom: 0;
  }
  .popper[x-placement^="bottom"],
  .tooltip[x-placement^="bottom"] {
	margin-top: 5px;
  }
  .tooltip[x-placement^="bottom"] .tooltip-arrow,
  .popper[x-placement^="bottom"] .popper__arrow {
	border-width: 0 5px 5px 5px;
	border-left-color: transparent;
	border-right-color: transparent;
	border-top-color: transparent;
	top: -5px;
	left: calc(50% - 5px);
	margin-top: 0;
	margin-bottom: 0;
  }
  .tooltip[x-placement^="right"],
  .popper[x-placement^="right"] {
	margin-left: 5px;
  }
  .popper[x-placement^="right"] .popper__arrow,
  .tooltip[x-placement^="right"] .tooltip-arrow {
	border-width: 5px 5px 5px 0;
	border-left-color: transparent;
	border-top-color: transparent;
	border-bottom-color: transparent;
	left: -5px;
	top: calc(50% - 5px);
	margin-left: 0;
	margin-right: 0;
  }
  .popper[x-placement^="left"],
  .tooltip[x-placement^="left"] {
	margin-right: 5px;
  }
  .popper[x-placement^="left"] .popper__arrow,
  .tooltip[x-placement^="left"] .tooltip-arrow {
	border-width: 5px 0 5px 5px;
	border-top-color: transparent;
	border-right-color: transparent;
	border-bottom-color: transparent;
	right: -5px;
	top: calc(50% - 5px);
	margin-left: 0;
	margin-right: 0;
  }

</style>


<link href='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/4.2.0/core/main.min.css' rel='stylesheet' />
<link href='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/4.2.0/daygrid/main.min.css' rel='stylesheet' />
<link href='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/4.2.0/list/main.min.css' rel='stylesheet' />


<script src='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/4.2.0/core/main.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/4.2.0/daygrid/main.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/fullcalendar/4.2.0/list/main.min.js'></script>

<script src='https://unpkg.com/popper.js/dist/umd/popper.min.js'></script>
<script src='https://unpkg.com/tooltip.js/dist/umd/tooltip.min.js'></script>
	
<script >

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
	plugins: [ 'dayGrid', 'list' ],
	defaultView: 'listWeek',
	defaultDate: '"""+today+"""',
	views: {
		listDay: { buttonText: 'list day' },
		listWeek: { buttonText: 'list week' },
		listMonth: { buttonText: 'list month' }
	  },
	header: {
	  left: 'prev,next today',
	  center: 'title',
	  right: 'dayGridMonth,listWeek,listDay'
	},
	eventRender: function(info) {
	  var tooltip = new Tooltip(info.el, {
		title: info.event.extendedProps.description,
		placement: 'top',
		trigger: 'hover',
		container: 'body'
	  });
	},
	events: 
	  """+ events_string +"""
	
  });

  calendar.render();
});

</script>

</head>
<body>
<center><h1>Calendar with Frankfurt playtimes of moviews in Original Version </h1></center>

<div id='calendar'></div>

<center>
<a href="https://www.buymeacoffee.com/ffmovkino" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a></center>
</center>

<br>

</body>
</html>

	"""

        #convert to byte
	html_byte = html_text.encode()


	
	start_response("200 OK", [
			("Content-Type", "text/html; charset=UTF-8"),
			("Content-Length", str(len(html_byte)))
	])
	return iter([html_byte])
