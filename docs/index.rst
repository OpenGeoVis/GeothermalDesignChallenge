################################
2019 Geothermal Design Challenge
################################


.. image:: https://img.shields.io/github/stars/OpenGeoVis/GeothermalDesignChallenge.svg?style=social&label=Stars
  :target: https://github.com/OpenGeoVis/GeothermalDesignChallenge
  :alt: GitHub

About
*****


This website outlines our work (see who we are on :ref:`meet_the_team`) for the
`2019 Geothermal Design Challenge`_ put on by the Department of Energy's Utah
FORGE Team.

.. _2019 Geothermal Design Challenge: https://utahforge.com/studentcomp/

All of the code to reproduce our figures and findings is included in the
`OpenGeoVis/GeothermalDesignChallenge`_ GitHub repository. The website
consolidates that code and our finding for others to learn about the the tools
we implemented and be able to reproduce our work.

.. _OpenGeoVis/GeothermalDesignChallenge: https://github.com/OpenGeoVis/GeothermalDesignChallenge


Summary
*******


Members of the W-Team have created a suite of open-source Python packages making
3D visualization more accessible to the geoscientific community - enabling
researchers to rapidly explore their data, communicate their spatial findings,
and facilitate reproducibility amongst stakeholders and colleagues.
This portfolio demonstrates the ability to tackle spatial questions through a
workflow that incrementally integrates available data and yields more insight as
new data is added to a 3D scene.

The tools used in this effort include tools maybe by W-Team members and other
open-source tools common in the geosciences:

- vtki: http://docs.vtki.org (W-Team)
- PVGeo: http://pvgeo.org (W-Team)
- The Open Mining Format: https://omf.readthedocs.io/en/latest/
- omfvtk: https://github.com/OpenGeoVis/omfvtk (W-Team)
- ParaView: http://paraview.org
- SGeMS: http://sgems.sourceforge.net
- SimPEG: http://www.simpeg.xyz


The modern open-source software paradigm has brought on the rise of countless
tools available to researchers - as users and developers of these tools, we
wrangled the project data into an emerging, open-source file specification:
the Open Mining Format (OMF).
Once we collected the FORGE site project data into the OMF specification, we
were able to seamlessly work across a range of software packages, creating
geostatistical models from the given temperature data, and running inversions of
the given geophysical data to produce regional-scale models and data products
that could be integrated into a single visualization environment for making
spatial decisions.


Report
******

Our team has made the entire project available for the geothermal community to
interact with our findings and reproduce the results shown in this portfolio.
Furthermore, a video is included where a team member immerses themselves into
the FORGE site’s data via Virtual Reality (VR) and directly engages with the
visualizations to address the question posed by the US Department of Energy’s
Utah FORGE team.


.. raw:: html

    <iframe src="https://player.vimeo.com/video/329706722" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>



The modern open-source software paradigm has brought on the rise of countless
tools available to researchers - coupling the increase in software availability
with new technologies like the VR, any scientists, including you reading this,
can access these tools and directly engage with data in a 3D environment.


Where do you target your next production well to maximize geothermal reservoir
performance at the FORGE site in Milford, Utah?  This is a challenging question
given not only the complex 3D subsurface but the multiple data attributes
available and their respective uncertainties.  Multidimensional visualization
aids researchers in their ability to gain insight from the spatial relationships
of their data as well as helps communicate how spatial decisions are made to a
broader, non-technical audience. The following visualization portfolio showcases
how 3D visualization can be used to make decisions and address the posed
question in a reproducible fashion.

Location: The FORGE site is located in an area of groundwater discharge and
contains a dry fluvial system that may seasonally fill and flow.
To minimize the environmental impact of the new well pad, our team proposes a
location within the site boundaries that is several meters away from any branch
of the seasonal river system, according to the topography map.
The X and Y Coordinates (UTM) of our proposed well are thus (334618, 4262018).
At this location, the granitoid layer will be reached at a greater depth,
providing a slightly easier drilling process. The subsurface location of the
well resembles that of well 58-32.

Depth: The constraints on depth included penetrating the granitoid layer and
being within 175º and 225º Celsius. Below the FORGE site, this required a depth
of at least 2000m. Our team searched for a region beneath the FORGE site near
this depth that would maximize the likelihood of producing from the target
temperature zone. Using the provided temperature probe data, our team created a
geostatistical model of subsurface temperature and compared isocontours of that
model with the provided temperature contours to ensure the proposed well
location had a consistent temperature range across the data sets. Our team chose
a depth of 2200m to surpass the 175ºC temperature threshold confidently.


Trajectory: Based on well trajectory data of Milford Valley, it appears that all
wells but 58-32 were drilled at a 90º dip, 0º azimuth. Even well 58-32 shows an
almost identical trajectory with very slight variation. Therefore, our new well
will have as close to a 90º dip, 0º azimuth trajectory as possible.


In summary, our recommendation for the new production well is shown in Table 1
of the attached supplemental materials.



.. toctree::
   :hidden:

   self
   team
   static-portfolio
   dynamic-portfolio
