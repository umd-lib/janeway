# Customstyling
A Janeway plugin that allows a staff member to add custom CSS directives to a journal or press site, giving the user control over the styling of each site.

## Installation Instructions
1. Clone this repository into the Janeway plugins folder (`path/to/janeway/src/plugins/`)
2. Run the plugin installation command: `python3 src/manage.py install_plugins customstyling`.
3. Restart your webserver

## CSS Variables

If your journal or press uses the OLH theme, you can quickly update the color palette of your journal with the following CSS template. Replace the color code used for each variable to match your desired output:
```
:root {
--primary-dark-color: #22175b; /* Primary colour used by elements such as buttons */
--very-dark-primary-color: #22175b;  /* Darker primary colour used for contrast or hover effects */
--primary-light-color: #fff; /* lighter colour or secondary colour */
--topbar-background-color: #FFF; /* background colour for the top bar of the navigation */
--menu-background-color: #FFFFFF; /* background colour for the menu bar of the navigation */
--menu-alternative-background-color: #FFFFFF; /* Alternative background colour for the menu bar, used by some buttons */
--menu-foreground-color: #000000; /* font colour used in the menu bar */
--link-color: #2199e8;
--toc-link-color: #22175b; /* Colour used by text on TOC sidebar elements */
--figure-caption-background-color: #003DAC; 
--figure-caption-color: #FFFFFF;
}
```

These variables do not work on the Material or Clean themes yet, though we have plans to add theses or similar variables for those themes.
