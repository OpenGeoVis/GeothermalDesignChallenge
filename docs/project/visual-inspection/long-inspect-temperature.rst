.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_project_visual-inspection_long-inspect-temperature.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_project_visual-inspection_long-inspect-temperature.py:


Inspect Temperature Model
~~~~~~~~~~~~~~~~~~~~~~~~~

This notebook examines the temperature model and shows off a useful PVGeo
algorithm for rmeove parts of a mesh/model that are baove a topographic surface.

.. code-block:: default


    # sphinx_gallery_thumbnail_number = 6

    # Import project package
    import gdc19








.. code-block:: default

    import pyvista
    import PVGeo
    import omfvista
    import pandas as pd
    import numpy as np







Load all the datasets created in the data aggreagation section


.. code-block:: default


    gis_data = omfvista.load_project(gdc19.get_project_path('gis.omf'))
    print(gis_data.keys())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ['boundary']



.. code-block:: default

    surfaces = omfvista.load_project(gdc19.get_project_path('surfaces.omf'))
    print(surfaces.keys())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ['land_surface', 'temp_225c', 'temp_175c', 'opal_mound_fault', 'negro_mag_fault', 'top_granitoid']



.. code-block:: default

    temperature_data = omfvista.load_project(gdc19.get_project_path('temperature.omf'))
    print(temperature_data.keys())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ['temperature', 'kriged_temperature_model']


Grab data from multi blocks for conveinance


.. code-block:: default

    topo = surfaces['land_surface']
    granitoid = surfaces['top_granitoid']

    p = pyvista.Plotter()
    p.add_mesh(topo)
    p.add_mesh(granitoid, color=True)
    p.show()




.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_001.png
    :class: sphx-glr-single-img




Note how the above figure has artificats from where the top of granite
surface boundary matches the topographic surface. To mitigate these effect,
we can use a filtering technique that will remove parts of a mesh above or
within a tolerance of a given surface. PVGeo has a filter that perfroms
this type of operation with ease.

Let's run a PVGeo filter to extract the topo surface from the granitoid
surface - :class:`PVGeo.grids.ExtractTopography`


.. code-block:: default


    # Run the PVGeo algorithm
    granitoid = PVGeo.grids.ExtractTopography(
                    remove=True, # remove the inactive cells
                    tolerance=10.0 # buffer around the topo surface
                ).apply(granitoid, topo)

    p = pyvista.Plotter()
    p.add_mesh(topo)
    p.add_mesh(granitoid, color=True)
    p.show()




.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_002.png
    :class: sphx-glr-single-img




Now both the topographic surface and the granitoid boundary can be rendered
without arficats due to where they overlap.

This type of topography extraction is often very useful with 3D models where
the model domain goes above the topographic surface - thus we may want to
parts of a 3D model above the topography. Let's try this with the temoerature
model.


.. code-block:: default


    temp_grid = temperature_data['kriged_temperature_model']

    temp_kwargs = dict(
        cmap='coolwarm',
        clim=temp_grid.get_data_range(),
        stitle='Temperature (C)'
    )







First, crop the model down to the FORGE region:


.. code-block:: default


    temp_grid_cropped = temp_grid.clip_box(gdc19.get_roi_bounds(), invert=False)
    temp_grid_cropped.plot(**temp_kwargs)




.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_003.png
    :class: sphx-glr-single-img




Now extract the topographic surface from the model to have a more realistic
domain:


.. code-block:: default


    # Remove values above topography
    temp_grid_no_topo = PVGeo.grids.ExtractTopography(
                    remove=True, # remove the inactive cells
                    tolerance=10.0 # buffer around the topo surface
                   ).apply(temp_grid_cropped, topo)

    temp_grid_no_topo.plot(**temp_kwargs)





.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_004.png
    :class: sphx-glr-single-img




Now lets find the temperature range of intereset: 175 to 225 degrees C


.. code-block:: default


    temp_roi = temp_grid_no_topo.threshold([175., 225.])
    temp_roi.plot(**temp_kwargs)




.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_005.png
    :class: sphx-glr-single-img




And just out of curiosity, how big of a volume is that temperature range?


.. code-block:: default

    print('Temperature Region is {:.2f} cubic kilometers.'.format(temp_roi.volume * 1e-9))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Temperature Region is 229.00 cubic kilometers.


How do the provided temperature surfaces match our geostatisical model?


.. code-block:: default


    temp_175c = surfaces['temp_175c']
    temp_225c = surfaces['temp_225c']

    p = pyvista.Plotter()
    p.add_mesh(temp_roi, opacity=0.7, **temp_kwargs)
    p.add_mesh(temp_175c, **temp_kwargs)
    p.add_mesh(temp_225c, **temp_kwargs)
    p.show()




.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_006.png
    :class: sphx-glr-single-img




Now lets put this all together to gain insight on where that temperature
plume is in relation to the FRGE site


.. code-block:: default


    boundary = gis_data['boundary']
    boundary_tube = PVGeo.filters.AddCellConnToPoints(cell_type=4,
                        close_loop=True).apply(boundary).tube(radius=30)

    p = pyvista.Plotter()
    p.add_mesh(topo, opacity=0.7)
    p.add_mesh(temp_roi, **temp_kwargs)
    p.add_mesh(granitoid, color=True)
    p.add_mesh(boundary_tube, color='yellow')
    p.show()



.. image:: /project/visual-inspection/images/sphx_glr_long-inspect-temperature_007.png
    :class: sphx-glr-single-img





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  52.166 seconds)


.. _sphx_glr_download_project_visual-inspection_long-inspect-temperature.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: long-inspect-temperature.py <long-inspect-temperature.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: long-inspect-temperature.ipynb <long-inspect-temperature.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
