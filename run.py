from __future__ import print_function, unicode_literals, absolute_import, division
import os
import sys
from shapely import wkt
from cytomine import CytomineJob
from cytomine.models import Annotation, AnnotationCollection, ImageInstanceCollection, Job


def main(argv):
    with CytomineJob.from_cli(argv) as conn:
        conn.job.update(status=Job.RUNNING, progress=0, statusComment="Initialization...")
        base_path = "{}".format(os.getenv("HOME"))
        working_path = os.path.join(base_path, str(conn.job.id))
        # Select images to process
        images = ImageInstanceCollection().fetch_with_filter("project", conn.parameters.cytomine_id_project)
        if conn.parameters.cytomine_id_images == 'all':
            list_imgs = [int(image.id) for image in images]
        else:
            list_imgs = [int(id_img) for id_img in conn.parameters.cytomine_id_images.split(',')]
        for image in images:
            if image.id in list_imgs:
                # to download preview photo
                image.dump(os.path.join(working_path, str(conn.parameters.cytomine_id_project), "{originalFilename}.jpg"))
                # todo: map.key=id map.value=filename
                print(image.filename)
                # To download the original files that have been uploaded to Cytomine image.download(os.path.join(
                # image.download(os.path.join(working_path, str(conn.parameters.cytomine_id_project), "{originalFilename}"))

        # Go over images
        for id_image in conn.monitor(list_imgs, prefix="Running detection on image", period=0.1):

            # Dump ROI annotations in img from Cytomine server to local images
            # conn.job.update(status=Job.RUNNING, progress=0, statusComment="Fetching ROI annotations...")
            roi_annotations = AnnotationCollection(
                terms=[conn.parameters.cytomine_id_roi_term],
                project=conn.parameters.cytomine_id_project,
                image=id_image,  # conn.parameters.cytomine_id_image
                showWKT=True,
                includeAlgo=True,
            )

            print(id_image)
            roi_annotations.fetch()
            print("roi_annotations:", roi_annotations)
            # Go over ROI in this image
            # for roi in conn.monitor(roi_annotations, prefix="Running detection on ROI", period=0.1):
            # for roi in roi_annotations:
            #     # todo:maybe need to skip the same location
            #     # Get Cytomine ROI coordinates for remapping to whole-slide
            #     # Cytomine cartesian coordinate system, (0,0) is bottom left corner
            #     print("----------------------------ROI------------------------------")
            #     roi_location = wkt.loads(roi.location)
            #     print("ROI Geometry from Shapely: {}".format(roi_location))
                # todo:analysis
            cytomine_annotations = AnnotationCollection()
            # Append to Annotation collection
            # for add location
            cytomine_annotations.append(Annotation(  # location=annotation.wkt,
                location="POLYGON ((36109.95549010582 147655.59850021894, 36109.55365096127 147653.51671169934, "
                         "36108.87777322558 147651.54945907506, 36107.39890407232 147650.07656870427, "
                         "36105.54027792273 147649.23347494105, 36103.88244593348 147648.6077553122, "
                         "36102.190285802586 147648.4958079435, 36100.702401460374 147648.45101637868, "
                         "36099.31099941644 147648.46120291104, 36097.984939886504 147648.78667316757, "
                         "36096.60099406466 147648.91339662686, 36095.09564080415 147649.15229220127, "
                         "36093.63301683809 147649.79678406956, 36091.795815871104 147650.46758802503, "
                         "36090.06123804619 147651.6836307092, 36088.83669658621 147653.46962929834, "
                         "36087.79030760816 147655.59850021894, 36088.06522408287 147657.8841702026, "
                         "36088.54977625958 147660.1530803143, 36090.290465022365 147661.75717428658, "
                         "36092.3277674899 147662.73390886842, 36094.37200813175 147663.1513018844, "
                         "36096.143105430754 147663.41313391406, 36097.82062323549 147663.2544023276, "
                         "36099.31099941644 147663.6401874228, 36100.82448129998 147663.3730955386, "
                         "36102.490534524135 147663.44185266065, 36104.11683505797 147662.9476781887, "
                         "36105.80479871247 147662.2338106529, 36107.45970378002 147661.1619418037, "
                         "36108.660928266545 147659.55576399848, 36109.31541844323 147657.6318687021, "
                         "36109.95549010582 147655.59850021894))",
                id_image=id_image,  # conn.parameters.cytomine_id_image,
                id_project=conn.parameters.cytomine_id_project,
                id_terms=[conn.parameters.cytomine_id_cell_term]))
            print(".", end='', flush=True)

                # Send Annotation Collection (for this ROI) to Cytomine server in one http request
            cytomine_annotations.save()

        conn.job.update(status=Job.TERMINATED, progress=100, statusComment="Finished.")


if __name__ == "__main__":
    main(sys.argv[1:])
