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
