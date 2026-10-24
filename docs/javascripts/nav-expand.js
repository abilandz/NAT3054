// Expand specific sections by matching their toggle IDs or labels:
// Example: In MkDocs "material" in the LHS menu, I want toggle "Lectures" to be expanded by default, 
//          and toggle "Homeworks" not.
document$.subscribe(function() {
  const expandSections = ['__nav_2']; // In my case. "Lectures" is the second menu item, after "Introduction"
                                      // if I want to specify more, use e.g. ['__nav_2', '__nav_3'], etc.
  document.querySelectorAll('.md-nav__toggle').forEach(toggle => {
    if (expandSections.some(id => toggle.id.includes(id))) {
      toggle.checked = true;
    }
  });
});
