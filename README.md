<!DOCTYPEhtml>
 <html lang="en-US">
  <body>

<h1>Morgan State Computer Science Medical Annotation Research</h1>

<h2>Design Princples</h2>
<ol>
	<li>OOP is used rather than Procedural Programming because it is faster
	to make a large data structure global to the instance of the class rather
	than pass by value.</li>
	<li id="DP2">The system is multi-threaded because each step of getting and formatting
	data does not need to wait for the previous step to finish. This will
	esure that large data sets get process as quickly as possible.</li>
</ol>

<h2>External Libraries Used</h2>
<ol>
	<li>The CV2 library is used to crop and save images that have unions.</li>
	<li>The WGET library is used to download all the images from the internet.</li>
	<li>The Pandas library is used to read and write data to and from CSV files.</li>
</ol>

<h2>Native Modules Used</h2>
<ol>
	<li>The OS module is used to check if the unfiltered CSV file exist and create needed directories.</li>
	<li>The Threading module is used to create multi-threaded work loads. See <a href="#DP2">Design Princple #2</a>.</li>
</ol>

<h2>How it Works</h2>
<ol>
	<li>Check if the user generated results file exists.</li>
	<li>Start threads to download images and get user generated response data.</li>
	<li>Downloading images thread uses the wget library to download all the images in the results CSV files.</li>
	<li>The get responses thead get all the selected keywords and store them in a file</li>
	<li>The main thread will create an instance of FindUnion and generate meta data constants.</li>
	<li>The cropping algorithm takes each users cropping value and puts them into 1D arrays to be used in the crop method.</li>
	<li>Crop each image according to the values stored in 1D array</li>
</ol>

 </body>
</html>
