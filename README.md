<!DOCTYPEhtml>
 <html lang="en-US">
  <body>

<h1>Morgan State Computer Science Medical Annotation Research</h1>
<p>This code is used for Morgan State University research. Dr. Rahman facilitated this research. This research is designed to help doctors better detect diseases in humans using ML. First, doctors compleate surveys via Amazon Mturk. Next, some algorithms get all the useful data. Lastly, this data is then used as inputs for a machine learning algorithm.</p>

<h2>How to Use</h2>
<ol>
	<li>To run the code run: <code>py3 CollectAnnotations.py fileLocation.csv</code>. <b>*NOTE*</b> Substitute <code>py</code> with whatever your system requires to run python.</li>
	<li>CollectAnnotations.py <b>MUST</b> recieve  at least one command line argument. Each argument <b>MUST</b> be a csv file.</li>
	<li>There are three optional arguments -o, -p, -h. -h means Help. If -h is anywhere in the list of args a help message is printed, then the python <b>WILL</b> exit with error code 0. -o is the number of questions that was asked to each user. -p is the location of a folder must where all the results will be saved. If -o and -p are used at the time then -o must supersede -p</li>
	<li>Example: <code>py3 CollectAnnotations.py fileLocation.csv fileLocation2.csv -o 25 -a \otherFileLocation\</code></li>
	<li>Example: <code>py3 CollectAnnotations.py -h</code></li>
</ol>

 </body>
</html>
