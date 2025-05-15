<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <!-- Header -->
  <header>
    <h1>Smart Telescope Project</h1>
    <p>Date: May 14, 2025</p>
    <p>Team Members: David Bascom (ddb73), Ajay Sunkara (aks237)</p>
    <p>This project seeks to help those who are bad at pointing a telescope themselves enjoy being able to still use there telescope and see distant planets up           close. It strives to take away any technical skill or high monitary limit from the anmature astronmers, and let whomever wants have an easy viewing                experience of the night sky</p>
    <img src="img/team_photo.jpg" alt="Team Photo" />
  </header>

  <!-- Navigation -->
  <nav>
    <ul>
      <li><a href="#objective">Objective</a></li>
      <li><a href="https://www.youtube.com/watch?v=et91Gea6CPk" target="_blank">Project Video</a></li>
      <li><a href="#introduction">Introduction</a></li>
      <li><a href="#design">Design & Testing</a></li>
      <li><a href="#results">Results</a></li>
      <li><a href="#conclusions">Conclusions</a></li>
      <li><a href="#future-work">Future Work</a></li>
      <li><a href="#budget">Budget</a></li>
      <li><a href="#references">References</a></li>
      <li><a href="#code">Code Appendix</a></li>
      <li><a href="#contributions">Contributions</a></li>
    </ul>
  </nav>

  <main>
    <!-- Introduction Section -->
    <section id="introduction">
      <h2>Introduction</h2>
      <p> This project had 3 significant aspects to it:mech anical, electical, and software. The mechanical side involved designing a new mount for a
      telescope that would be motorized in 2 axes to allow it to point anywhere in the night sky. The main conciderations here were avoiding colisions and               ensuring the motors had enough torque. This was acomplished by offsetting the mount for the scope behind the first rotational axis, and implimenting a 
      4:1 belt drive system. </p>
      <p>On the electical side, we needed the ability to drive 2 brushless motors, ensure positional feedback, automatically get GPS 
        location and heading, have a touch screen controller, and power everything. For our motor drivers we used the mjbots moteus c1 driver, which comunicates 
        over CANFD. To suport this off the pi, we also used the mjbots usb-canfd converter. For heading and GPS, we used the Berry-GPS-IMU-4. Our touchscreen was 
        a cheap amazon pi monitor that uses HTMI for signal and USB for power. The pi was powered off a cell phone charger via USB-C, and the motion system is 
        powered using a 6s Lipo battery. </p>
      <p>As for the software, we used two librarys: Skyfield and moteus. Upon startup, the mount takes in the current heading, and zeros the first axis to face 
        due 
        north. The second axis is automatically zeroed baced on its position at startup, which it assumes to be level with the ground. When a user selects a
        target (such as a planet or the moon) from the touch screen GUI, the name of that target, the current GPS location, and the current time are given to 
        Skyfield. Skyfield gives us back degrees in the altitude and azimuth, which we then translate into motor rotations for each axis. We then use moteus to 
        convert those rotations into a CANFD message, and send it over the CAN line</p>
    </section>
    <!-- Design and Testing Section -->
    <section id="design">
      <h2>Design & Testing</h2>
      <p>Mechanically, all parts of this project are 3D printed. Linear Rods from an old 3D printer are used to rienforce the prints to make them stronger.
      Large breakings are also used on both rotational axes to ensure smooth opperation. The design is made in 21 individual 3D prints, and assembled using 
      linear rods and M3 screws. This part of the project went pretty smoothly. Asside from a few print failures, a bit of trouble getting the bearings to sit
      properly in thier press fit housing, and one of the prints being the wrong size, and requiring a reprint. </p>
      <p>Electically, things also went pretty smoothly. Soldering the motors to the boards directly reduced costs for connectors. To power the boards, we made 
      a custom wire harness to split power from the Lipo into two connectors. Similarly, CAN is also split after the converter board. These all required quite 
      a bit of soldering. The pi is simply plugged into the phone charger, and the touch screen into the pi.We had a weird issue where the touch screen would not
      work with certain USB ports/cables, but this issue was fixed by switching out the USB cable that connected to the screen. The IMU is a pihat, which did 
      require us to remove the piTFT and reconfigure the pi to boot without it. Later, we discovered that the on board GPS antenna did not work, even outdoors,
      and decided not to use it </p>
      <p>Software is definitly where we had the most issues. Querrying data from the IMU was pretty simple to impliment, but it took us quite a while of messing 
      with the software to figure out that we were not the issue, but the hardware was. After figuring this out, we ditched it entirely, and set the telescope up
      so that it would auto zero in the startup position. Implimenting the GUI went decently smoothly, but took a relatively long time due to the number of 
      targets that we needed to be able to see. This was a large part of the reason why the 7 in touch screen was choosen, as the piTFT was MUCH too small for
      this. The real chalenge was figuring out what the actual targets are. Skyfield has a number of files you can download that each have differnt targets in 
      them. We wanted to be able to automatically see what the targets in the file were, extract them, turn them into a human readable name, and send that back
      to the library. We did this so that different files could be loaded and any new targets would still apear on the GUI. To do this, however, we did spend a
      considerable amount of time figuring out how to extract target names, auto-renaming everything into something that made sense to humans, and automatically,
      laying out the GUI buttons baced on the number of targets available in a file. </p>
      <p> During testing we dicovered several things. The first of which was that a lot of the entries in the skyfield files point to random points in the 
        universe called "baricenters". These are centers of gravitational attraction, and there is nothing there. We ended up having to filter these out of the 
      valid targets that could be displayed on the GUI. Furthermore, we discovered that the the motors we selected we not very precice. While this was not an 
      issue when looking at objects that were large or close by (like the moon), objects that did not fit those criteria were in many cases completely out of the 
      telescope's view. Unfortunatly, this did come down to a physical limitation of the motor, and was not something we could fix</p>
    </section>
    <!-- Results Section -->
    <section id="results">
      <h2>Results</h2>
      <p><!-- Did everything perform as planned? Goals met? --></p>
    </section>
    <!-- Conclusions Section -->
    <section id="conclusions">
      <h2>Conclusions</h2>
      <p><!-- Project achievements and failures --></p>
    </section>
    <!-- Future Work Section -->
    <section id="future-work">
      <h2>Future Work</h2>
      <p><!-- Exploration if more time allowed --></p>
    </section>
    <!-- Budget Section -->
    <section id="budget">
      <h2>Budget</h2>
      <ul>
        <!-- List parts and costs here -->
      </ul>
    </section>
    <!-- References Section -->
    <section id="references">
      <h2>References</h2>
      <ul>
        <!-- Cite datasheets, papers, websites, class materials -->
      </ul>
    </section>
    <!-- Code Appendix Section -->
    <section id="code">
      <h2>Code Appendix</h2>
      <p>See <a href="https://github.com/your-repo-link">code repository</a> for full listings.</p>
      <pre><code>
// Example code snippet
// ...
      </code></pre>
    </section>

    <!-- Contributions Section -->
    <section id="contributions">
      <h2>Team Contributions</h2>
      <ul>
        <li>Alice: Mechanical design and prototyping</li>
        <li>Bob: Electronics integration and firmware</li>
        <li>Charlie: Software control and UI</li>
      </ul>
    </section>
  </main>

  <!-- Footer -->
  <footer>
    <p>&copy; 2025 Smart Telescope Team, Cornell University</p>
  </footer>
</body>
</html>
