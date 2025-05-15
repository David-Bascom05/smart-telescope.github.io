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
      <p>< This project had 3 significant aspects to it:mech anical, electical, and software. The mechanical side involved designing a new mount for a
      telescope that would be motorized in 2 axes to allow it to point anywhere in the night sky. The main conciderations here were avoiding colisions and               ensuring the motors had enough torque. This was acomplished by offsetting the mount for the scope behind the first rotational axis, and implimenting a 
      4:1 belt drive system
        
      On the electical side, we needed the ability to drive 2 brushless motors, ensure positional feedback, automatically get GPS location and heading, have a
      touch screen controller, and power everything. For our motor drivers we used the mjbots moteus c1 driver, which comunicates over CANFD. To suport this off
      the pi, we also used the mjbots usb-canfd converter. For heading and GPS, we used the Berry-GPS-IMU-4. Our touchscreen was a cheap amazon pi monitor that
      uses HTMI for signal and USB for power. The pi was powered off a cell phone charger via USB-C, and the motion system is powered using a 6s Lipo battery
      
      As for the software, we used two librarys: Skyfield and moteus. Upon startup, the mount takes in the current heading, and zeros the first axis to face due
      north. The second axis is automatically zeroed baced on its position at startup, which it assumes to be level with the ground. When a user selects a target 
      (such as a planet or the moon) from the touch screen GUI, the name of that target, the current GPS location, and the current time are given to Skyfield.   
      Skyfield gives us back degrees in the altitude and azimuth, which we then translate into motor rotations for each axis. We then use moteus to convert those
      rotations into a CANFD message, and send it over the CAN line  ></p>
    </section>

    <!-- Design and Testing Section -->
    <section id="design">
      <h2>Design & Testing</h2>
      <p><!-- Design steps, issues, testing methods --></p>
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
