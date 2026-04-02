# Datacom AI Workplace - Full Portfolio Submission

# Store Locator Feature - Exploration Report
**Prepared by:** Mike (Graduate Associate)
**Prepared for:** Maya (Product Lead) & Client

## 1. Client Request Summary
The client has requested a new "Store Locator" feature for their existing website. The primary goal is to allow users to easily find the nearest physical store locations by entering their postcode. To be successful, this feature needs to be intuitive, fast, and fully mobile-responsive.

## 2. Proposed Features & Components
To build a functional and user-friendly Store Locator, we will need the following key components:
- **Search Input Field:** A text field for the user to input their postcode, city, or suburb.
- **'Use My Location' Button:** A button that leverages the browser's device Geolocation API to auto-detect the user's current location via GPS.
- **Search Trigger:** A standard search button or real-time filtering as the user types.
- **Interactive Map Area:** A dynamic map (e.g., Google Maps API or Mapbox) with pins displaying store locations.
- **Results List Panel:** A scrollable text list showing the nearest stores, including details like distance, address, phone number, working hours, and a clear "Get Directions" link.
- **Backend/Database:** A dataset of store locations with geographical coordinates (latitude and longitude) that can be queried against the user's location.

## 3. Code Snippets & Exploration
Here is a simplified, mobile-friendly HTML & JavaScript structure for the Store Locator interface, designed logically with frontend best practices.

### HTML Structure
```html
<div class="store-locator-container">
  <div class="search-section">
    <h2>Find a Store Near You</h2>
    <div class="search-bar">
      <input type="text" id="postcode-input" placeholder="Enter your postcode..." />
      <button id="search-btn">Search</button>
      <button id="geo-btn" aria-label="Use my current location">📍 My Location</button>
    </div>
  </div>
  
  <div class="results-section">
    <div id="map-container">
      <!-- Map integration goes here -->
      <div class="map-placeholder">Interactive Map View</div>
    </div>
    <ul id="store-list">
      <!-- Dynamically populated store results go here -->
      <li class="store-item">
        <h3>Datacom HQ Store</h3>
        <p>123 Tech Lane (0.5 miles)</p>
        <p>Open until 8:00 PM</p>
        <a href="#">Get Directions</a>
      </li>
    </ul>
  </div>
</div>
```

### CSS (Mobile-Friendly Design Foundation)
```css
/* Mobile-first CSS */
.store-locator-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 15px;
}
.search-bar {
  display: flex;
  flex-wrap: wrap; /* Allows wrapping on very small smartphone screens */
  gap: 10px;
}
#postcode-input {
  flex: 1; /* Takes up remaining space seamlessly */
  padding: 12px;
  font-size: 16px; /* Prevents auto-zoom on iOS Safari */
  border-radius: 6px;
  border: 1px solid #ccc;
}
button {
  padding: 12px 18px;
  background-color: #0056b3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.results-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* Desktop enhancement (Responsive UI) */
@media (min-width: 768px) {
  .results-section {
    flex-direction: row;
  }
  #map-container { flex: 2; height: 500px; }
  #store-list { flex: 1; overflow-y: auto; height: 500px; }
}
```

**Why this code works:**
It uses a "mobile-first" CSS approach, heavily leveraging modern `flexbox`. On mobile screens, the search bar, the map, and the store list will stack vertically logically without horizontal scrolling. On wider screens (tablets/desktops), the `@media` query activates and triggers the map and results to display side-by-side. The input font size is set strictly to `16px` to ensure mobile browsers (like iOS Safari) don’t awkwardly zoom in when the user taps to type.

## 4. UI Description & Sketch
**Visualizing the Interface:**
- **Top banner:** A clean, full-width search bar labeled "Find a Store Near You". It has a magnifying glass icon inside the input and a subtle "Use current location" crosshair icon button next to it.
- **Below the banner (Mobile view):** The map takes up the upper 50% of the screen. The bottom 50% is a vertically scrollable list of store cards. Each card has a clean white background with a subtle shadow (`box-shadow`), bolding the store name, showing the distance in a bright accent color, and featuring a prominent "Directions" button.
- **Below the banner (Desktop view):** The map takes up the left 60% of the screen. The right 40% contains the scrollable list of store cards so users can view the map and the list simultaneously. 

## 5. Client Summary Email Draft
**Subject:** Store Locator Feature - Exploration & Planning Update

Hi [Client Name],

I hope you're having a great week!

Our team at Datacom has been exploring the integration of the new Store Locator feature for your website. Maya asked me to share a quick update on our preliminary planning and what we envision for the component to ensure it perfectly aligns with your goals.

**Overview of our approach:**
- **Seamless user experience:** Users will be able to simply type in their postcode or click a "Use My Location" button to instantly see their closest stores.
- **Mobile-optimized:** The feature is designed "mobile-first", meaning it will look and perform flawlessly on smartphones, with a layout that scales beautifully to desktops.
- **Interactive Results:** We're planning an interactive split-view design with a live map on one side and actionable store cards (including opening hours and a "Get Directions" link) on the other.

**Next Steps & Proposed Timeline:**
- [ ] **Week 1:** Finalize UI/UX design mockups for your approval.
- [ ] **Week 2:** Backend database setup for store coordinates and map API integration.
- [ ] **Week 3:** Front-end development and mobile responsiveness checks. 
- [ ] **Week 4:** Quality assurance testing and deployment.

Please let us know if you have any feedback on this initial direction. We look forward to bringing this feature to life!

Best regards,

**Mike**  
Graduate Associate | Datacom 
(On behalf of Maya & the Development Team)


<div style="page-break-after: always;"></div>

# Task 1: Reflect and Review

**Completed by:** Mike (Graduate Associate)

### 1. How did the AI help you break down the task?
Working with the AI as a collaborative partner made the ambiguous task of "exploring a Store Locator" highly structured. By asking for specific components, the AI quickly generated an organized list of functional requirements (like Geolocating and mapping) that I might not have logically sequenced right away. Instead of staring at a blank page, the AI served as a powerful brainstorming engine that provided a comprehensive skeleton for the client report. It also seamlessly connected the technical requirements (code structure) with the visual requirements (UI sketch).

### 2. What did you learn about writing prompts that include context and goals?
I learned that providing detailed context (e.g., stating the user is a non-technical product planner, naming my manager Maya, and defining the specific deliverables like an email and code snippets) directly influenced the tone and relevance of the AI's output. When goals are explicitly defined in the prompt, the AI stops giving generic "textbook" answers and starts generating targeted, workplace-ready artifacts. The structure of "What (task), Why (context), How (format)" is incredibly effective.

### 3. How could you use AI to support future client requests?
In the future, I can use AI at the very beginning of the project lifecycle to rapidly prototype ideas and summarize lengthy client requirement documents. If a client asks for a complex new feature, I can prompt the AI to define the minimum viable components, draft initial communication emails for stakeholder alignment, and even outline potential technical roadblocks for our senior developers. Essentially, AI becomes an accelerator for the foundational research and communication phases of any project.


<div style="page-break-after: always;"></div>

# 🏙️ Riverland City Council: Community Innovation Forum
**Topic:** Improving Public Services with Emerging Technologies
**Drafted by:** Mike & Datacom AI Partner

---

## Slide 1: Emerging Tech Trends in Local Government
![Smart City Ecosystem](images/slide_1.png)

**Key Technologies Transforming Public Services:**
1. **The Internet of Things (IoT):** Networks of connected sensors collecting real-time data from city infrastructure (like streetlights and water pipes).
2. **Artificial Intelligence (AI):** Systems that analyze massive amounts of city data to predict trends, automate responses, and optimize resource allocation.
3. **Smart Infrastructure:** Physical assets built with embedded technology to adapt to environmental changes instantly.

🗣️ **Speaker Notes:**
> *"Welcome, everyone. Today we are exploring how emerging technology isn't just about flashy gadgets—it's about fundamentally improving the services we rely on every day. Three key technologies are leading this charge: IoT sensors that give our city 'nervous systems', AI that acts as the 'brain' to process data, and Smart Infrastructure that physically adapts to community needs in real-time."*

---

## Slide 2: Primary Community Challenges
![Challenges Icons](images/slide_2.png)

**What are we trying to solve?**
- **🚦 Traffic Congestion:** Growing populations are overwhelming traditional intersections and transit routes, leading to delays and pollution.
- **♻️ Waste Management Inefficiencies:** Static garbage collection schedules lead to overflowing public bins and wasted fleet fuel on empty bins.
- **🛡️ Public Safety & Emergency Response:** First responders face delays navigating unpredictable urban obstacles and routing issues.

🗣️ **Speaker Notes:**
> *"Before we talk about solutions, we must ground ourselves in the actual challenges our growing Riverland community faces. As our population expands, we're seeing increased bottlenecks in traffic, inefficiencies in how we handle waste management, and the need for rapidly deploying emergency services through busy streets. These are the core targets we want to address."*

---

## Slide 3: Tech-Enabled Solutions & Next Steps
![Tech Roadmap](images/slide_3.png)

**The Smart City Roadmap:**
1. **Traffic Optimization:** AI analyzes data from IoT cameras to instantly alter traffic light patterns, clearing bottlenecks dynamically.
2. **Smart Waste Fleets:** Sensors inside public bins notify management *only* when full, optimizing the route of waste collection vehicles.
3. **Automated Emergency Routing:** Smart infrastructure communicates with emergency vehicles to clear traffic pathways in real-time.

**Next Steps / Call to Action:**
🎯 **Recommendation:** Establish a 'Smart City Pilot Group' starting next month to trial IoT traffic sensors at our 3 busiest intersections.

🗣️ **Speaker Notes:**
> *"How do we bridge the gap? By pairing the technologies from slide one with the problems from slide two. AI can reprogram traffic lights in real-time to alleviate congestion. IoT sensors can tell our waste trucks exactly which bins need emptying, saving fuel. Our recommendation to action this today is to launch a Smart City Pilot Group next month, focusing initially on traffic sensors at our three worst intersections to prove immediate ROI."*

---

<div style="page-break-after: always;"></div>

# Task 2: Reflect and Review

**Completed by:** Mike (Graduate Associate)

### 1. What tasks did AI help with most?
AI was most helpful in accelerating the content creation and visual ideation phases. Specifically, it excelled at synthesizing complex, technical concepts (like IoT, AI, and Smart Infrastructure) into concise, non-technical bullet points suitable for a public city council presentation. It significantly reduced the time required to brainstorm an organized sub-topic flow for the slides, allowing me to focus on refining the speaker notes and overall narrative instead of starting from scratch.

### 2. How did you guide the AI to get better results?
I guided the AI by using an iterative prompting approach. When the initial output was a bit too generic or academic, I refined my prompts by adding specific constraints to the persona—such as defining the target audience (Riverland City Council and local residents) and requesting a persuasive, accessible tone. I also found that explicitly asking the AI to split the output into "Slide Content" and "Speaker Notes" yielded a much more structured and presentation-ready result.

### 3. What would you do differently next time?
Next time, I would provide even more upfront constraints in my initial prompt, such as strict word counts per slide or a specific slide layout structure, to reduce the number of revision cycles. I would also consider using "few-shot prompting" by providing the AI with a short example of the exact tone or format I am aiming for right from the beginning, ensuring the first draft is much closer to the final product.

<div style="page-break-after: always;"></div>

# Task 3: Problem Solving & Debugging

**Prepared by:** Mike (Graduate Associate)
**Prepared for:** Maya (Product Lead)

---

## Deliverable: Internal Summary Email to Maya

**Subject:** Issue Identified & Fixed: Client Contact Us Form Not Submitting Correctly

Hi Maya,

I've investigated the issue the client flagged regarding their "Contact Us" form failing to submit correctly. I treated this like a puzzle and used AI to help track down the bug without needing a software engineering background!

**What the issue was:**
The main bug was a small but critical missing attribute in the HTML. The email input field was written as `<input type="email">`, missing the `name="email"` attribute. Because of this, when a user clicked "Send", their email address was entirely left out of the submitted data package, breaking the form's ability to process the inquiry correctly. Additionally, the `<form>` tag itself was missing an `action` attribute (which tells the form where to send the data) and a `method` attribute (like POST).

**How AI helped me identify and solve it:**
I provided my AI partner with the exact HTML code and prompted it with: *"What's wrong with this code? The client says the form isn't submitting correctly. Can you explain the issue simply and help rewrite it?"* 
The AI quickly highlighted that the `name` attribute was missing from the email tag and explained in plain English that HTML forms rely on `name` attributes as standard labels to pass data. It then supplied a cleaned-up, fully structured version of the code.

**The corrected version of the code:**
```html
<!DOCTYPE html> 
<html>
<head>  
  <title>Contact Us</title> 
</head> 
<body>  
  <h2>Contact Us</h2>  
  <!-- Added action, method, and cleaned up form fields with the missing name attribute -->
  <form action="/submit-message" method="POST">    
    <label for="name">Name:</label> 
    <input type="text" id="name" name="name" required><br>    
    
    <label for="email">Email:</label> 
    <input type="email" id="email" name="email" required><br>    
    
    <label for="message">Message:</label> 
    <textarea id="message" name="message" required></textarea><br>    
    
    <button type="submit">Send</button>  
  </form> 
</body> 
</html>
```

**Brief reflection on testing & learning:**
To verify the fix, I saved the original code locally as `contact.html` and opened it in my browser to see the error in action. When I submitted the original, I noticed the URL query string was missing the email data entirely. After replacing it with the AI's corrected code, I tested it again and saw form submission behavior work exactly as intended. 

I learned that debugging isn't always about writing complex logical pipelines; it's often about reading code for its intent, noticing tiny grammatical inconsistencies (like a missing word), and asking clear, focused questions to guide an AI towards the solution.

Let me know if I should package this up and pass it over to Sam to finalize deployment to the client's live site!

Best regards,

**Mike**
Graduate Associate | Datacom
