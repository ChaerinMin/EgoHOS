# inference
python predict_image.py \
       --config_file ./work_dirs/seg_twohands_ccda/seg_twohands_ccda.py \
       --checkpoint_file ./work_dirs/seg_twohands_ccda/best_mIoU_iter_56000.pth \
       --img_dir ../myimages/images \
       --pred_seg_dir ../myimages/pred_twohands \

python predict_image.py \
       --config_file ./work_dirs/twohands_to_cb_ccda/twohands_to_cb_ccda.py \
       --checkpoint_file ./work_dirs/twohands_to_cb_ccda/best_mIoU_iter_76000.pth \
       --img_dir ../myimages/images \
       --pred_seg_dir ../myimages/pred_cb

python predict_image.py \
       --config_file ./work_dirs/twohands_cb_to_obj1_ccda/twohands_cb_to_obj1_ccda.py \
       --checkpoint_file ./work_dirs/twohands_cb_to_obj1_ccda/best_mIoU_iter_34000.pth \
       --img_dir ../myimages/images \
       --pred_seg_dir ../myimages/pred_obj1

# visualize
python visualize.py \
       --mode twohands \
       --img_dir ../myimages/images \
       --twohands_dir ../myimages/pred_twohands \
       --vis_dir ../myimages/pred_twohands_vis

python visualize.py \
       --mode cb \
       --img_dir ../myimages/images \
       --cb_dir ../myimages/pred_cb \
       --vis_dir ../myimages/pred_cb_vis

python visualize.py \
       --mode twohands_obj1 \
       --img_dir ../myimages/images \
       --twohands_dir ../myimages/pred_twohands \
       --obj1_dir ../myimages/pred_obj1 \
       --vis_dir ../myimages/pred_obj1_vis

