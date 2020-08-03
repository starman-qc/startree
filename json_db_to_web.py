"""
x_list = [1, -2, 3, 4]
y_list = [10, 11, -12, 13]
text_list = ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100']
color_list = ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)']
size_list = [10, 5, 7, 100]
"""
import json, math
x_list = []
y_list = []
text_list = []
color_list = []
size_list = []
pi = + 3.1416
with open('star_db_4.json') as f:
  data = json.load(f)

for star in data:
    x_list.append(data[star][0])
    y_list.append(data[star][1])
    text_list.append(star)
    rad_raw = math.atan2(data[star][0], data[star][1])
    rad = ((rad_raw+pi)/(2*pi))
    color_r = 255 - min(abs(rad-0.49)%1, abs((rad-1)-0.49)%1)*2*255
    color_g = 255 - min(abs(rad-0.82)%1, abs((rad-1)-0.82)%1)*2*255
    color_b = 255 - min(abs(rad-0.16)%1, abs((rad-1)-0.16)%1)*2*255
    color_list.append(f'rgb({color_r}, {color_g}, {color_b})')
    size_list.append(data[star][2])
page = """<meta name="robots" content="noindex">
<head>
	<!-- Load plotly.js into the DOM -->
	<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
</head>
<body>
	<div id='myDiv'><!-- Plotly chart will be drawn inside this DIV --></div>
<script id="jsbin-javascript">
var trace1 = {{
  x: {},
  y: {},
  text: {},
  mode: 'markers',
  marker: {{
    color: {},
    size: {}
  }}
}};
var data = [trace1];
var layout = {{
  title: 'Star Tree map',
  plot_bgcolor:"black",
  paper_bgcolor:"#FFF3",
  showlegend: false,
  height: 1200,
  width: 1200
}};
Plotly.newPlot('myDiv', data, layout);
</script>
</body>
""".format(x_list, y_list, text_list, color_list, size_list)

print(page)
text_file = open("page.html", "w")
n = text_file.write(page)
text_file.close()