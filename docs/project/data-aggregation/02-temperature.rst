.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_project_data-aggregation_02-temperature.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_project_data-aggregation_02-temperature.py:


Temperature Data
~~~~~~~~~~~~~~~~


.. code-block:: default

    # sphinx_gallery_thumbnail_number = 4
    # Import project package
    import gdc19








.. code-block:: default

    import pyvista
    import PVGeo
    import omf
    import omfvista
    import pandas as pd
    import numpy as np








Temperature Probe Data
++++++++++++++++++++++


.. code-block:: default


    # Load the temperature data
    _temp = pd.read_csv(
                gdc19.get_temperature_path('well_based_temperature.csv')
                )
    _temp.head()








.. code-block:: default

    temperature = omf.PointSetElement(
        name='temperature',
        description='cumulative record of one-dimensional temperature modeling '\
            'based off of well data. Temperature log data were exampled and '\
            'extrapolated below the bottom of a number of wells. Temperatures '\
            'are in degrees Celsius, and all location data are georeferenced to '
            'UTM, zone 12N, NAD 83, NAVD 88.',
        subtype='point',
        geometry=omf.PointSetGeometry(
            vertices=_temp[['x', 'y', 'z']].values
        ),
        data=[omf.ScalarData(
            name='temperature (C)',
            array=_temp['T'].values,
            location='vertices'
        ),]
    )
    temperature.validate()









.. code-block:: default

    temp = omfvista.wrap(temperature)
    temp.plot()





.. image:: /project/data-aggregation/images/sphx_glr_02-temperature_001.png
    :class: sphx-glr-single-img




Geostatistical Model
++++++++++++++++++++

Prep temperature data for kriging in SGeMS


.. code-block:: default


    # First, load the topography surface that was previously aggregated:
    surfaces = omfvista.load_project(gdc19.get_project_path('surfaces.omf'))
    topo = surfaces['land_surface']


    p = pyvista.Plotter()
    p.add_mesh(temp, cmap='coolwarm', point_size=10,
               render_points_as_spheres=True, stitle='Temperature')
    p.add_mesh(topo)
    p.camera_position = [1,1,-1]
    p.show()




.. image:: /project/data-aggregation/images/sphx_glr_02-temperature_002.png
    :class: sphx-glr-single-img




Make tables of the temperature and topography data


.. code-block:: default


    # Make pandas data frame of the temps
    df_temp = pd.DataFrame(data=np.c_[temp.points, temp.point_arrays['temperature (C)']],
                        columns=['x', 'y', 'z', 'temp_c'])
    df_temp.header = 'temperature (degrees C)'
    print(df_temp.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

               x           y       z  temp_c
    0  339385.01  4264212.99  1680.6   150.0
    1  339385.01  4264212.99   880.6   195.0
    2  339385.01  4264212.99  -119.4   195.0
    3  337709.02  4260660.00  1596.3   250.0
    4  337709.02  4260660.00   796.3   262.0




.. code-block:: default


    # And of the topography surface
    df_topo = pd.DataFrame(data=topo.points, columns=['x','y','z'])
    df_topo.header = 'Land Surface'
    print(df_topo.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

                   x             y            z
    0  329924.988160  4.270951e+06  1493.691650
    1  329924.988160  4.270926e+06  1493.996460
    2  329949.993331  4.270926e+06  1493.786011
    3  329949.993331  4.270951e+06  1493.691650
    4  329974.998501  4.270926e+06  1493.790039



Save these tabular data frames to GSLib formatted files for use in SGeMS


.. code-block:: default


    gdc19.save_gslib(gdc19.get_krig_path('temperature.gslib'), df_temp)
    gdc19.save_gslib(gdc19.get_krig_path('topography.gslib'), df_topo)







Load the kriged temperature model from SGeMS


.. code-block:: default


    fkrig = gdc19.get_krig_path("Geotherm_kriged_0.sgems")
    fvar = gdc19.get_krig_path("Geotherm_kriged_0_krig_var.sgems")

    # Read the kirgged model and variance
    grid = PVGeo.gslib.SGeMSGridReader().apply(fkrig)
    grid_var = PVGeo.gslib.SGeMSGridReader().apply(fvar)

    # Label the array appropriately
    grid.rename_scalar('Getherm_kriged_0', 'Temperature')
    grid.cell_arrays['Temperature_var'] = grid_var.cell_arrays['Getherm_kriged_0_krig_var']







Set the spatial reference of the grid
Values from SGeMS:


.. code-block:: default

    grid.origin = (325000, 4.245e6, -2700)
    grid.spacing = (250, 250, 50)

    grid.plot(cmap='coolwarm')




.. image:: /project/data-aggregation/images/sphx_glr_02-temperature_003.png
    :class: sphx-glr-single-img




Lets quickly inspect the model


.. code-block:: default


    bounds = gdc19.get_roi_bounds()
    clipped = grid.clip_box(bounds, invert=False)

    contours = clipped.cell_data_to_point_data().contour()
    contours.plot(cmap='coolwarm', clim=clipped.get_data_range())





.. image:: /project/data-aggregation/images/sphx_glr_02-temperature_004.png
    :class: sphx-glr-single-img




Now we need to convert the model to the OMF files specification


.. code-block:: default


    # MINUS ONE BECASE WE DEFINE CELL DATA
    ncx, ncy, ncz = np.array(grid.dimensions) - 1
    sx, sy, sz = grid.spacing


    temp_model = omf.VolumeElement(
            name='kriged_temperature_model',
            description='kriged temoerature model built from temperature probe data',
            geometry=omf.VolumeGridGeometry(
                tensor_u=np.full(ncx, sx),
                tensor_v=np.full(ncy, sy),
                tensor_w=np.full(ncz, sz),
                origin=grid.origin,
            ),
            data=[omf.ScalarData(
                    name='temperature (C)',
                    array=grid.cell_arrays['Temperature'].reshape((ncz,ncy,ncx), order='F').ravel(),
                    location='cells'),
                  omf.ScalarData(
                    name='Temperature_var',
                    array=grid.cell_arrays['Temperature_var'].reshape((ncz,ncy,ncx), order='F').ravel(),
                    location='cells'),
                 ],
    )
    temp_model.validate()







And one final sanity check


.. code-block:: default


    omfvista.wrap(temp_model).clip_box(gdc19.get_roi_bounds(), invert=False).plot(cmap='coolwarm')





.. image:: /project/data-aggregation/images/sphx_glr_02-temperature_005.png
    :class: sphx-glr-single-img




Write the data
++++++++++++++


.. code-block:: default


    proj = omf.Project(
        name='FORGE Temperature Data',
        description='All temperature data/models for the 2019 FORGE Geothermal Student Competition '
    )

    proj.elements = [ temperature,  temp_model]

    proj.validate()







Save the temperature project file


.. code-block:: default


    omf.OMFWriter(proj, gdc19.get_project_path('temperature.omf'))







.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  44.880 seconds)


.. _sphx_glr_download_project_data-aggregation_02-temperature.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: 02-temperature.py <02-temperature.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: 02-temperature.ipynb <02-temperature.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
