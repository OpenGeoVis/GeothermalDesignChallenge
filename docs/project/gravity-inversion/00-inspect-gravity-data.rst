.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_project_gravity-inversion_00-inspect-gravity-data.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_project_gravity-inversion_00-inspect-gravity-data.py:


Inspect Gravity Data
~~~~~~~~~~~~~~~~~~~~

Here we take a look at what gravity data is available for the FORGE site


.. code-block:: default

    # sphinx_gallery_thumbnail_number = 2
    import gdc19

    import pandas as pd
    import pyvista
    import omfvista








.. code-block:: default

    df = pd.read_csv(gdc19.get_gravity_path('Utah_FORGE_Gravity_Data.txt'))
    print(df.keys())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Index(['FID', 'FID_', 'name', 'lon', 'lat', 'easting', 'northing', 'HAE',
           'NGVD29', 'obs', 'errg', 'iztc', 'oztc', 'gFA', 'gSBGA', 'gCBGA',
           'Source'],
          dtype='object')



Make a mapping between scalar names and their descriptions


.. code-block:: default

    field_desc = {
        "name": "the individual gravity station name.",
        "lon": "station Longitude, WGS84",
        "lat": "station latitude, WGS84",
        "easting": "UTM zone 12 easting, NAD83",
        "northing": "UTM zone 12 northing, NAD83",
        "HAE": "height above ellipsoid [meter]",
        "NGVD29": "vertical datum for geoid [meter]",
        "obs": "observed gravity",
        "errg": "gravity measurement error [mGal]",
        "iztc": "inner zone terrain correction [mGal]",
        "oztc": "outer zone terrain correction [mGal]",
        "gFA": "free air gravity",
        "gSBGA": "Bouguer horizontal slab",
        "gCBGA": "Complete Bouguer anomaly",
        "Source": "data source",
    }








.. code-block:: default

    ref = ['easting', 'northing', 'HAE']
    points = df[ref]
    for name in ref:
        df.pop(name)
    grav_obs = pyvista.PolyData(points.values)
    grav_obs.point_arrays.update(df.to_dict('series'))

    grav_obs = grav_obs.clip_box(gdc19.get_roi_bounds(), invert=False)

    print(grav_obs)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    UnstructuredGrid (0x7ff8989cdca8)
      N Cells:      786
      N Points:     781
      X Bounds:     3.301e+05, 3.441e+05
      Y Bounds:     4.253e+06, 4.271e+06
      Z Bounds:     1.488e+03, 2.706e+03
      N Arrays:     14





.. code-block:: default

    grav_obs.plot(scalars='gCBGA', stitle=field_desc['gCBGA'])




.. image:: /project/gravity-inversion/images/sphx_glr_00-inspect-gravity-data_001.png
    :class: sphx-glr-single-img





.. code-block:: default


    # Load the topography surface that was previously aggregated:
    surfaces = omfvista.load_project(gdc19.get_project_path('surfaces.omf'))
    topo = surfaces['land_surface']








.. code-block:: default

    p = pyvista.Plotter()
    p.add_mesh(topo)
    p.add_mesh(grav_obs, scalars='gCBGA', point_size=10.0,
              render_points_as_spheres=True, stitle=field_desc['gCBGA'])
    p.show()




.. image:: /project/gravity-inversion/images/sphx_glr_00-inspect-gravity-data_002.png
    :class: sphx-glr-single-img




Save gravity data for processing in next example


.. code-block:: default

    grav_obs.save(gdc19.get_gravity_path('grav_obs.vtk'))







.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  15.252 seconds)


.. _sphx_glr_download_project_gravity-inversion_00-inspect-gravity-data.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: 00-inspect-gravity-data.py <00-inspect-gravity-data.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: 00-inspect-gravity-data.ipynb <00-inspect-gravity-data.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
