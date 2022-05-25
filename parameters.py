# --Parameters:
imsize = 416  # Image dimensions
thresh = 0.3  # Confidence threshold for bounding
source = './run_detections/single_image/'  # Path to image to run detections on
weight_ccz = './model/logo_best.pt'  # Pretrained weights for deteections
weight_wli = './model/cc-z-best.pt'  # Pretrained weights for deteections
weight_all = '../model/all_weights.pt'  # All detections, lower performance
#outpath = './runs/detect/'
test_img_folder = 'LR/*'
detect_type = 0  # change later
#filename = 'test.jpg'
