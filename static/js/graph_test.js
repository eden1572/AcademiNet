// נתחיל על ידי יצירת נתוני גרף פשוטים
const data = [10, 20, 30, 40, 50];

// יצירת סולם מדידה לגרף
const scale = d3.scaleLinear()
  .domain([0, d3.max(data)]) // קביעת תחום הערכים של הנתונים
  .range([0, 300]); // קביעת תחום ההצגה בגרף

// יצירת מחולל עיגון
const axis = d3.axisLeft(scale);

// הוספת הסולם ל-svg
d3.select("svg")
  .append("g")
  .attr("transform", "translate(50,10)")
  .call(axis);

// הוספת עמודות ל-svg
d3.select("svg")
  .selectAll("rect")
  .data(data)
  .enter()
  .append("rect")
  .attr("x", (d, i) => i * 70)
  .attr("y", (d) => 300 - scale(d))
  .attr("width", 50)
  .attr("height", (d) => scale(d))
  .attr("fill", "teal");
