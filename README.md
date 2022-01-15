<!DOCTYPEhtml>
 <html lang="en-US">
  <body>

<h1>Morgan State Computer Science Medical Annotation Research</h1>
<p>This code is used for Morgan State University research. Dr. Rahman facilitated this research. This research is designed to help doctors better detect diseases in humans using ML. First, doctors compleate surveys via Amazon Mturk. Next, some algorithms get all the useful data. Lastly, this data is then used as inputs for a machine learning algorithm.</p>

<h2>How to Use</h2>
<p><b>Note:</b> Ensure Pandas is version 1.3, or greater</p>

<h3>Collect Annotations</h3>
<ol>
	<li>To run the code run: <code>py3 CollectAnnotations.py fileLocation.csv</code>. <br /><b>*NOTE*</b> Substitute <code>py</code> with whatever your system requires to run python.</li>
	<li>CollectAnnotations.py can take as many batch file command line arguments as needed.</li>
	<li>CollectAnnotations.py <b>MUST</b> recieve  at least one command line argument. Each argument <b>MUST</b> be a csv file.</li>
	<li>There are two optional arguments -s and -h. -h means Help. If -h is anywhere in the list of args a help message is printed, then the python <b>WILL</b> exit with error code 0. -s is the location of a folder must where all the results will be saved.</li>
</ol>

<h3>Create Batches</h3>
<ol>
	<li>To run the code: <code>py3 createBatches.py batchLocation.csv -l [number]</code></li>
	<li>createBatches.py <b>MUST</b> take -l as an argument. It is the last index that was read from the last time createBatches.py was run, or the index that createBatches should start from.</li>
	<li>-s is an optional argument. It is the location where the results from createBatches.py will be saved. If it is not passed a Batches folder will be created and all output files will be saved there.</li>
	<li>-h means help. If this argument is anywere in the list of arguments a help message will be printed and the code will exit with error code 0.</li>
	<li>-c is the index to end at and it is exclusive. The value to end at is calulated by adding -l's values + -c's value. If -c is not passed 101 is assumed.</li>
</ol>

<h2>Examples</h2>

<h3>Collect Annotations</h3>
<ol>
	<li><code>py3 CollectAnnotations.py fileLocation.csv</code></li>
	<li><code>py3 CollectAnnotations.py fileLocation.csv fileLocation2.csv -a \otherFileLocation\</code></li>
	<li><code>py3 CollectAnnotations.py -h</code></li>
</ol>

<h3>Create Batches</h3>
<ol>
	<li><code>py3 createBatches.py batchLocation.csv -l [number]</code></li>
	<li><code>py3 createBatches.py batchLocation.csv -l [number] -s [filePath/]</code></li>
	<li><code>py3 createBatches.py batchLocation.csv -l [number] -c [number]</code></li>
</ol>

 </body>
</html>