##############################################################################
Data to Decisions: An Open-Source Approach to 3D Visualization & Communication
##############################################################################


.. image:: https://img.shields.io/travis/OpenGeoVis/GeothermalDesignChallenge/master.svg?label=build&logo=travis
   :target: https://travis-ci.org/OpenGeoVis/GeothermalDesignChallenge

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

.. comment:

    You can also launch this project on Binder!

    .. image:: https://mybinder.org/badge_logo.svg
       :target: https://mybinder.org/v2/gh/OpenGeoVis/GeothermalDesignChallenge/master

.. toctree::
   :hidden:
   :caption: About

   self
   team


Summary
*******


Bane Sullivan has created a suite of open-source Python
packages making 3D visualization more accessible to the geoscientific community
- enabling researchers to rapidly explore their data, communicate their spatial
findings, and facilitate reproducibility amongst stakeholders and colleagues.
This portfolio demonstrates the ability to tackle spatial questions through a
workflow that incrementally integrates available data and yields more insight as
new data is added to a 3D scene.

The tools used in this effort include tools made by Bane and other open-source
software common in the geosciences:

- vtki: http://docs.vtki.org (Bane Sullivan)
- PVGeo: http://pvgeo.org (Bane Sullivan)
- The Open Mining Format: https://omf.readthedocs.io/en/latest/
- omfvtk: https://github.com/OpenGeoVis/omfvtk (Bane Sullivan)
- ParaView: http://paraview.org
- SGeMS: http://sgems.sourceforge.net
- SimPEG: http://www.simpeg.xyz


The modern open-source software paradigm has brought on the rise of countless
tools available to researchers - as users and developers of these tools, we
wrangled the project data into an emerging, open-source file specification:
the `Open Mining Format (OMF)`_.
Once we collected the FORGE site project data into the OMF specification, we
were able to seamlessly work across a range of software packages, creating
geostatistical models from the given temperature data, and running inversions of
the given geophysical data to produce regional-scale models and data products
that could be integrated into a single visualization environment for making
spatial decisions.


.. _Open Mining Format (OMF): https://omf.readthedocs.io/en/stable/


Portfolio
*********

Our team has made the entire project available for the geothermal community to
interact with our findings and reproduce the results shown in this portfolio.
Furthermore, a video is included where a team member immerses themselves into
the FORGE site’s data via Virtual Reality (VR) and directly engages with the
visualizations to address the question of where to place a new production well
posed by the US Department of Energy’s Utah FORGE team.


.. raw:: html

    <iframe src="https://player.vimeo.com/video/329706722" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>



.. toctree::
   :hidden:
   :caption: Portfolio

   portfolio/index
   portfolio/static
   portfolio/dynamic




.. toctree::
   :hidden:
   :caption: Reproducible Project

   project/index
