point_cloud_range = [-54.0, -54.0, -5.0, 54.0, 54.0, 3.0]
class_names = [
    'car', 'truck', 'construction_vehicle', 'bus', 'trailer', 'barrier',
    'motorcycle', 'bicycle', 'pedestrian', 'traffic_cone'
]
voxel_size = [0.075, 0.075, 0.2]
out_size_factor = 8
evaluation = dict(interval=2)
dataset_type = 'NuScenesDataset_wCam'
data_root = 'data/nuscenes/'
input_modality = dict(
    use_lidar=True,
    use_camera=True,
    use_radar=False,
    use_map=False,
    use_external=False)
img_scale = (800, 448)
num_views = 6
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
depth_sine_L = 1
virtual_depth=False
train_pipeline = [
    dict(
        type='LoadPointsFromFile',
        coord_type='LIDAR',
        load_dim=5,
        use_dim=[0, 1, 2, 3, 4],
    ),
    dict(
        type='LoadPointsFromMultiSweeps',
        sweeps_num=10,
        use_dim=[0, 1, 2, 3, 4],
    ),
    dict(type='MyLoadAnnotations3D', with_bbox_3d=True, with_label_3d=True, with_bbox=True, with_label=True, with_centers=True, with_cam_bbox=True, with_visible=True),
    dict(type='LoadMultiViewImageFromFiles'),
    dict(
        type='OurGlobalRotScaleTrans',
        rot_range=[-0.3925 * 2, 0.3925 * 2],
        scale_ratio_range=[0.9, 1.1],
        translation_std=[0.5, 0.5, 0.5],
        virtual_depth=virtual_depth
    ),
    dict(
        type='OurRandomFlip3D',
        sync_2d=False,
        flip_ratio_bev_horizontal=0.5,
        flip_ratio_bev_vertical=0.5),
    # dict(type='PhotoMetricDistortionMultiViewImage', swap_channel=False),
    dict(type='OurRandomAffine', scaling_ratio_range=(0.9, 1.1), flip_ratio=0.5, flip_sync_3d=True),
    dict(type='MyResize', img_scale=img_scale, keep_ratio=True),
    dict(type='MyNormalize', **img_norm_cfg),
    dict(type='MyPad', size_divisor=32),
    dict(type='SparseDepth', scale_factors=[4], exp_time=0, depth_sine_L=depth_sine_L, virtual_depth=virtual_depth),
    # dict(type='SparseDepth', scale_factors=[1], depth_mean=0, depth_var=1),
    dict(type='PointsRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='OurObjectRangeFilter', point_cloud_range=point_cloud_range),
    dict(type='ObjectNameFilter', classes=class_names),
    dict(type='PointShuffle'),
    dict(type='DefaultFormatBundle3D', class_names=class_names),
    dict(type='Collect3D', keys=['points', 'img', 'gt_bboxes_3d', 'gt_labels_3d', 'gt_bboxes', 'gt_labels', 'gt_pts_centers_2d', 'gt_img_centers_2d', 'gt_bboxes_cam_3d', 'sparse_depth', 'gt_visible_3d', 'gt_bboxes_lidar'])
]
test_pipeline = [
    dict(
        type='LoadPointsFromFile',
        coord_type='LIDAR',
        load_dim=5,
        use_dim=[0, 1, 2, 3, 4],
    ),
    dict(
        type='LoadPointsFromMultiSweeps',
        sweeps_num=10,
        use_dim=[0, 1, 2, 3, 4],
    ),
    dict(type='LoadMultiViewImageFromFiles'),
    dict(
        type='MultiScaleFlipAug3D',
        img_scale=img_scale,
        pts_scale_ratio=1,
        flip=False,
        transforms=[
            dict(
                type='GlobalRotScaleTrans',
                rot_range=[0, 0],
                scale_ratio_range=[1.0, 1.0],
                translation_std=[0, 0, 0]),
            dict(type='RandomFlip3D'),
            dict(type='MyResize', img_scale=img_scale, keep_ratio=True),
            dict(type='MyNormalize', **img_norm_cfg),
            dict(type='MyPad', size_divisor=32),
            dict(type='SparseDepth', scale_factors=[4], depth_sine_L=depth_sine_L, virtual_depth=virtual_depth),
            # dict(type='SparseDepthCompletion', scale_factors=[4], virtual_depth=virtual_depth),
            # dict(type='SparseDepth', scale_factors=[1], depth_mean=0, depth_var=1),
            dict(
                type='DefaultFormatBundle3D',
                class_names=class_names,
                with_label=False),
            dict(type='Collect3D', keys=['points', 'img', 'sparse_depth'])
        ])
]
# test_pipeline = [
#     dict(
#         type='LoadPointsFromFile',
#         coord_type='LIDAR',
#         load_dim=5,
#         use_dim=[0, 1, 2, 3, 4],
#     ),
#     dict(
#         type='LoadPointsFromMultiSweeps',
#         sweeps_num=10,
#         use_dim=[0, 1, 2, 3, 4],
#     ),
#     dict(type='LoadMultiViewImageFromFiles'),
#     dict(
#         type='MultiScaleFlipAug3D',
#         img_scale=img_scale,
#         pts_scale_ratio=1,
#         flip=True,
#         pcd_horizontal_flip=True,
#         pcd_vertical_flip=True,
#         pts_rotation=[0.0, 0.109, -0.109, 0.218, -0.218],
#         transforms=[
#             dict(
#                 type='OurGlobalRotScaleTrans',
#                 rot_range=[0, 0],
#                 scale_ratio_range=[1.0, 1.0],
#                 translation_std=[0, 0, 0]),
#             dict(
#                 type='OurRandomFlip3D',
#                 sync_2d=False,
#                 flip_ratio_bev_horizontal=0,
#                 flip_ratio_bev_vertical=0),
#             dict(type='OurRandomAffine', scaling_ratio_range=(1, 1), flip_ratio=0, flip_sync_3d=True),
#             dict(type='MyResize', img_scale=img_scale, keep_ratio=True),
#             dict(type='MyNormalize', **img_norm_cfg),
#             dict(type='MyPad', size_divisor=32),
#             dict(type='SparseDepth', scale_factors=[4], exp_time=0, depth_sine_L=depth_sine_L, virtual_depth=virtual_depth),
#             # dict(type='SparseDepth', scale_factors=[1], depth_mean=0, depth_var=1),
#             dict(
#                 type='DefaultFormatBundle3D',
#                 class_names=class_names,
#                 with_label=False),
#             dict(type='Collect3D', keys=['points', 'img', 'sparse_depth'])
#         ])
# ]
data = dict(
    samples_per_gpu=3,
    workers_per_gpu=4,
    train=dict(
        type='CBGSDataset',
        dataset=dict(
            type=dataset_type,
            data_root=data_root,
            num_views=num_views,
            ann_file=data_root + '/nuscenes_infos_trainval_with_proj2d_wbox3dCL_vis_woRange.pkl',
            # ann_file=data_root + '/nuscenes_infos_val_with_proj2d_wbox3dCL_vis_woRange.pkl',
            load_interval=1,
            pipeline=train_pipeline,
            classes=class_names,
            modality=input_modality,
            test_mode=False,
            box_type_3d='LiDAR')),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        num_views=num_views,
        # ann_file=data_root + '/nuscenes_infos_val_with_gt2d.pkl',
        ann_file=data_root + '/nuscenes_infos_val_with_proj2d_wbox3dCL_vis_woRange.pkl',
        load_interval=1,
        pipeline=test_pipeline,
        classes=class_names,
        modality=input_modality,
        test_mode=True,
        box_type_3d='LiDAR'),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        num_views=num_views,
        # ann_file=data_root + '/nuscenes_infos_val_with_gt2d.pkl',
        ann_file=data_root + '/nuscenes_infos_val_with_proj2d_wDepth_woRange.pkl',
        # ann_file=data_root + '/nuscenes_infos_test.pkl',
        load_interval=1,
        pipeline=test_pipeline,
        classes=class_names,
        modality=input_modality,
        test_mode=True,
        box_type_3d='LiDAR'))
model = dict(
    type='ImplicitFusionDetector_3D_Cam_MS',
    freeze_img=False,
    batch_scaling='none',
    encode_depth_input=False,
    # img_backbone=dict(
    #     type='ResNet',
    #     depth=50,
    #     num_stages=4,
    #     out_indices=(0, 1, 2, 3),
    #     frozen_stages=1,
    #     in_channels=3,
    #     norm_cfg=dict(type='BN', requires_grad=True),
    #     norm_eval=True,
    #     style='pytorch',
    # ),
    img_backbone=dict(
        type='SwinTransformer',
        embed_dims=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        mlp_ratio=4,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.,
        attn_drop_rate=0.,
        drop_path_rate=0.2,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        with_cp=False,
        convert_weights=True,
    ),
    img_neck=dict(
        type='FPN',
        # in_channels=[256, 512, 1024, 2048],
        in_channels=[96, 192, 384, 768],
        out_channels=256,
        num_outs=5),
    pts_voxel_layer=dict(
        max_num_points=10,
        voxel_size=voxel_size,
        max_voxels=(120000, 160000),
        point_cloud_range=point_cloud_range),
    pts_voxel_layer_height=dict(
        max_num_points=100,
        voxel_size=[voxel_size[0]*out_size_factor, voxel_size[1]*out_size_factor, point_cloud_range[5]-point_cloud_range[2]],
        max_voxels=30000,
        point_cloud_range=point_cloud_range),
    pts_voxel_encoder=dict(
        type='HardSimpleVFE',
        num_features=5,
    ),
    pts_middle_encoder=dict(
        type='SparseEncoder',
        in_channels=5,
        sparse_shape=[41, 1440, 1440],
        output_channels=128,
        order=('conv', 'norm', 'act'),
        encoder_channels=((16, 16, 32), (32, 32, 64), (64, 64, 128), (128, 128)),
        encoder_paddings=((0, 0, 1), (0, 0, 1), (0, 0, [0, 1, 1]), (0, 0)),
        block_type='basicblock'),
    pts_backbone=dict(
        type='SECOND',
        in_channels=256,
        out_channels=[128, 256],
        layer_nums=[5, 5],
        layer_strides=[1, 2],
        norm_cfg=dict(type='BN', eps=0.001, momentum=0.01),
        conv_cfg=dict(type='Conv2d', bias=False)),
    pts_neck=dict(
        type='SECONDFPN',
        in_channels=[128, 256],
        out_channels=[256, 256],
        upsample_strides=[1, 2],
        norm_cfg=dict(type='BN', eps=0.001, momentum=0.01),
        upsample_cfg=dict(type='deconv', bias=False),
        use_conv_for_no_stride=True),
    pts_bbox_head=dict(
        type='ImplicitHead2D_Cam_MS_Deform',
        with_pts=True,
        with_img=True,
        pts_smca=False,
        num_views=num_views,
        in_channels_img=256,
        out_size_factor_img=4,
        num_proposals=200,
        num_img_proposals=200,
        in_channels=256 * 2,
        hidden_channel=128,
        num_classes=len(class_names),
        num_pts_decoder_layers=1,
        num_img_decoder_layers=1,
        num_fusion_decoder_layers=1,
        num_heads=8,
        initialize_by_heatmap=True,
        cross_heatmap=True,
        cross_only=True,
        cross_type='deform_height',
        depth_for_proposal=True,
        fuse_bev_feature=False,
        img_heatmap_dcn=False,
        cross_heatmap_dcn=False,
        cross_heatmap_LN=True,
        img_heatmap_LN=True,
        cross_heatmap_layer=1,
        img_heatmap_layer=2,
        # heatmap_query_level='max',
        cat_point=False,
        img_reg_layer=3,
        learnable_query_pos=False,
        nms_kernel_size=3,
        img_nms_kernel_size=3,
        ffn_channel=256,
        dropout=0.1,
        bn_momentum=0.1,
        activation='relu',
        projection='layernorm',
        supervision3d=True,
        stop_grad=False,
        fuse_projection=True,
        use_camera='se',
        img_reg_bn=False,
        reg_bn=True,
        # use_camera=None,
        cross_heatmap_stop_grad=False,
        img_heatmap_stop_grad=False,
        cross_heatmap_trick='none',
        fuse_self=True,
        common_heads=dict(center=(2, 2), height=(1, 2), dim=(3, 2), rot=(2, 2), vel=(2, 2)),
        level_num=4,
        sep_level_pos=False,
        encode_depth=True,
        depth_encoder='resnet',
        depth_encoder_dcn=False,
        view_transform=True,
        view_transform_pos_early=False,
        view_transform_point=False,
        view_transform_FFN=False,
        view_transform_point_proj=False,
        view_transform_rematch=True,
        view_bbox_add=False,
        bbox_pos=True,
        query_dropout=0.0,
        double_gt=False,
        fusion_gate=False,
        fusion_cwa=False,
        ignorance_loss=False,
        auxliary_loss=True,
        depth_input_channel=depth_sine_L*2,
        detection_2d=False,
        laplace_loss=False,
        allocentric=False,
        fuse_cat=False,
        virtual_depth=virtual_depth,
        bbox_coder=dict(
            type='TransFusionBBoxCoder',
            pc_range=point_cloud_range[:2],
            voxel_size=voxel_size[:2],
            out_size_factor=out_size_factor,
            post_center_range=[-61.2, -61.2, -10.0, 61.2, 61.2, 10.0],
            score_threshold=0.0,
            code_size=10,
        ),
        bbox_2d_coder=dict(
            type='CameraBBoxCoder',
            code_size=10,
        ),
        loss_cls=dict(type='FocalLoss', use_sigmoid=True, gamma=2, alpha=0.25, reduction='mean', loss_weight=1.0),
        # loss_iou=dict(type='CrossEntropyLoss', use_sigmoid=True, reduction='mean', loss_weight=0.0),
        loss_bbox=dict(type='L1Loss', reduction='mean', loss_weight=0.25),

        loss_depth_reg=dict(type='L1Loss', loss_weight=0.25),

        loss_heatmap=dict(type='GaussianFocalLoss', reduction='mean', loss_weight=0.1),
        loss_heatmap_2d=dict(type='GaussianFocalLoss', reduction='mean', loss_weight=0.1),
        loss_cls_2d=dict(type='FocalLoss', use_sigmoid=True, gamma=2, alpha=0.25, reduction='mean', loss_weight=1.0),
        loss_bbox_2d=dict(type='L1Loss', reduction='mean', loss_weight=0.25),
        loss_center_2d=dict(type='L1Loss', reduction='mean', loss_weight=5.0),
        loss_depth_laplace=dict(type='LaplaceL1Loss', reduction='mean', loss_weight=0.25)

        # loss_depth=dict(type='CrossEntropyLoss', use_sigmoid=False, reduction='mean', loss_weight=1.0),
        # loss_depth=dict(type='FocalLoss', use_sigmoid=True, gamma=2, alpha=0.25, reduction='mean', loss_weight=1.0),
    ),
    train_cfg=dict(
        pts=dict(
            dataset='nuScenes',
            assigner=dict(
                type='HungarianAssigner3D',
                iou_calculator=dict(type='BboxOverlaps3D', coordinate='lidar'),
                cls_cost=dict(type='FocalLossCost', gamma=2, alpha=0.25, weight=0.15),
                reg_cost=dict(type='BBoxBEVL1Cost', weight=0.25),
                iou_cost=dict(type='IoU3DCost', weight=0.25)
            ),
            assigner_2d=dict(
                type='HungarianAssignerCameraBox',
                iou_calculator=dict(type='BboxOverlaps3D', coordinate='camera'),
                cls_cost=dict(type='FocalLossCost', gamma=2, alpha=0.25, weight=0.15),
                reg_cost=dict(type='BBoxBEVL1Cost', weight=0.25),
                iou_cost=dict(type='IoU3DCost', weight=0.25),
            ),
            # assigner_2d=dict(
            #     type='HungarianAssignerView2D',
            #     cls_cost=dict(type='FocalLossCost', weight=2.0),
            #     reg_cost=dict(type='BBoxL1Cost', weight=5.0, box_format='xywh'),
            #     iou_cost=dict(type='IoUCost', iou_mode='giou', weight=2.0)
            # ),
            pos_weight=-1,
            gaussian_overlap=0.1,
            gaussian_overlap_2d=0.1,
            min_radius=2,
            max_radius=999,
            grid_size=[1440, 1440, 40],  # [x_len, y_len, 1]
            voxel_size=voxel_size,
            out_size_factor=out_size_factor,
            code_weights=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.2, 0.2],
            point_cloud_range=point_cloud_range)),
    test_cfg=dict(
        pts=dict(
            dataset='nuScenes',
            grid_size=[1440, 1440, 40],
            img_scale=img_scale,
            out_size_factor=out_size_factor,
            pc_range=point_cloud_range,
            voxel_size=voxel_size,
            nms_type='circle',
            use_rotate_nms=True,
            nms_thr=0.7,
            max_num=500
        )))
optimizer = dict(
    type='AdamW',
    # lr=0.00075,
    lr=0.00004,
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys={
            'img_backbone': dict(lr_mult=0.1),
            'img_neck': dict(lr_mult=0.1),
            'pts_voxel_layer': dict(lr_mult=0.1),
            'pts_voxel_encoder': dict(lr_mult=0.1),
            'pts_middle_encoder': dict(lr_mult=0.1),
            'pts_backbone': dict(lr_mult=0.1),
            'pts_neck': dict(lr_mult=0.1),
            'pts_bbox_head.point_transformer': dict(lr_mult=0.1),
            'pts_bbox_head.class_encoding': dict(lr_mult=0.1),
            'pts_bbox_head.heatmap_head': dict(lr_mult=0.1),
            'pts_bbox_head.shared_conv': dict(lr_mult=0.1),
            'absolute_pos_embed': dict(decay_mult=0.),
            'relative_position_bias_table': dict(decay_mult=0.),
            'norm': dict(decay_mult=0.)
        }),
)  # for 8gpu * 2sample_per_gpu
optimizer_config = dict(grad_clip=dict(max_norm=0.1, norm_type=2))
# optimizer_config = dict(grad_clip=dict(max_norm=35, norm_type=2))

# lr_config = dict(
#     policy='CosineAnnealing',
#     warmup='linear',
#     warmup_iters=500,
#     warmup_ratio=1.0 / 3,
#     min_lr_ratio=1e-3,
#     by_epoch=False
#     )

lr_config = dict(
    policy='cyclic',
    target_ratio=(10, 0.0001),
    cyclic_times=1,
    step_ratio_up=0.4,
    # warmup='linear',
    # warmup_iters=500,
    # warmup_ratio=1.0 / 3,
    )
momentum_config = dict(
    policy='cyclic',
    target_ratio=(0.8947368421052632, 1),
    cyclic_times=1,
    step_ratio_up=0.4)
total_epochs = 6
checkpoint_config = dict(interval=1)
log_config = dict(
    interval=50,
    hooks=[dict(type='TextLoggerHook'),
           dict(type='TensorboardLoggerHook')])
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = None
# load_from = 'checkpoints/LC_fusion_voxel0075_R50_20pc.pth'
# load_from = 'checkpoints/LC_Implicitfusion_voxel0075_R50_20pc.pth'
# load_from = 'checkpoints/LC_Implicitfusion_wohead_voxel0075_R50_20pc.pth'
load_from = 'checkpoints/LC_Implicitfusion_MSMDFusion_voxel0075_SwinT_mask_trainval.pth'
resume_from = None
workflow = [('train', 1)]
gpu_ids = range(0, 8)
freeze_lidar_components = True
find_unused_parameters = True
