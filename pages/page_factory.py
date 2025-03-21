import inspect
import types

from ATFramework.utils.log import logger
from pages.main_page import Main_Page
from pages.mask_designer_page import Mask_designer
from pages.media_room_page import Media_Room
from pages.title_room_page import Title_room
from pages.title_designer_page import Title_Designer
from pages.precut_page import Precut
from pages.video_speed_page import Video_speed_page
from pages.effect_room_page import Effect_Room
from pages.transition_room_page import Transition_room
from pages.import_downloaded_media_from_cl_page import Import_Downloaded_Media_From_CL
from pages.pip_designer_page import Pip_Designer
from pages.particle_room_page import Particle_room
from pages.library_preview_page import Library_Preview
from pages.timeline_operation_page import Timeline_Operation
from pages.playback_window_page import Playback_window
from pages.audio_mixing_room_page import Audio_Mixing_Room
from pages.pip_room_page import Pip_room
from pages.download_from_cl_dz_page import DownloadFromCLDZ
from pages.tips_area_page import Tips_area
from pages.preferences_page import Preferences_Page
from pages.video_collage_designer_page import VideoCollageDesigner
from pages.produce_page import Produce
from pages.voice_over_recording_page import Voice_Over_Recording_Room
from pages.fix_enhance_page import FixEnhance
from pages.keyframe_room import KeyFrame_Page
from pages.download_from_shutterstock_page import Shutterstock
from pages.blending_mode_page import Blending
from pages.upload_cloud_dz_page import Upload_Cloud_DZ
from pages.trim_page import Trim
from pages.particle_designer_page import Particle_Designer
from pages.crop_zoom_pan_page import Crop_Zoom_Pan
from pages.pan_zoom_page import Pan_Zoom
from pages.nest_project_page import Nest_Project
from pages.project_room_page import Project_Room
from pages.project_new_page import Project_New
from pages.gettyimage_page import Getty_Image
from pages.shape_designer_page import Shape_Designer
from pages.intro_video_room_page import Intro_Video_Room
from pages.crop_image_page import Crop_Image
from pages.subtitle_room_page import Subtitle_Room
from pages.audio_editing_page import Audio_Editing
from pages.motion_tracker_page import Motion_Tracker
from pages.effect_settings_page import Effect_Settings

class PageFactory():
    """ PageFactory uses the factory design pattern.  """

    @staticmethod
    def get_page_object(page_name, driver):
        # Return the appropriate page object based on page_name
        page_obj = None
        page_name = page_name.lower()
        if page_name == 'main_page':
            page_obj = Main_Page(driver)
        elif page_name == 'mask_designer_page':
            page_obj = Mask_designer(driver)
        elif page_name == 'media_room_page':
            page_obj = Media_Room(driver)
        elif page_name == 'title_room_page':
            page_obj = Title_room(driver)
        elif page_name == 'effect_room_page':
            page_obj = Effect_Room(driver)
        elif page_name == 'title_designer_page':
            page_obj = Title_Designer(driver)
        elif page_name == 'audio_mixing_room_page':
            page_obj = Audio_Mixing_Room(driver)
        elif page_name == 'library_preview_page':
            page_obj = Library_Preview(driver)
        elif page_name == 'timeline_operation_page':
            page_obj = Timeline_Operation(driver)
        elif page_name == 'import_downloaded_media_from_cl_page':
            page_obj = Import_Downloaded_Media_From_CL(driver)
        elif page_name == 'pip_designer_page':
            page_obj = Pip_Designer(driver)
        elif page_name == 'precut_page':
            page_obj = Precut(driver)
        elif page_name == 'video_speed_page':
            page_obj = Video_speed_page(driver)
        elif page_name == 'voice_over_recording_page':
            page_obj = Voice_Over_Recording_Room(driver)
        elif page_name == 'transition_room_page':
            page_obj = Transition_room(driver)
        elif page_name == 'particle_room_page':
            page_obj = Particle_room(driver)
        elif page_name == 'playback_window_page':
            page_obj = Playback_window(driver)
        elif page_name == 'pip_room_page':
            page_obj = Pip_room(driver)
        elif page_name == 'download_from_cl_dz_page':
            page_obj = DownloadFromCLDZ(driver)
        elif page_name == 'preferences_page':
            page_obj = Preferences_Page(driver)
        elif page_name == 'tips_area_page':
            page_obj = Tips_area(driver)
        elif page_name == 'video_collage_designer_page':
            page_obj = VideoCollageDesigner(driver)
        elif page_name == 'produce_page':
            page_obj = Produce(driver)
        elif page_name == 'keyframe_room_page':
            page_obj = KeyFrame_Page(driver)
        elif page_name == 'fix_enhance_page':
            page_obj = FixEnhance(driver)
        elif page_name == 'download_from_shutterstock_page':
            page_obj = Shutterstock(driver)
        elif page_name == 'blending_mode_page':
            page_obj = Blending(driver)
        elif page_name == 'upload_cloud_dz_page':
            page_obj = Upload_Cloud_DZ(driver)
        elif page_name == 'trim_page':
            page_obj = Trim(driver)
        elif page_name == 'particle_designer_page':
            page_obj = Particle_Designer(driver)
        elif page_name == 'crop_zoom_pan_page':
            page_obj = Crop_Zoom_Pan(driver)
        elif page_name == 'pan_zoom_page':
            page_obj = Pan_Zoom(driver)
        elif page_name == 'nest_project_page':
            page_obj = Nest_Project(driver)
        elif page_name == 'project_room_page':
            page_obj = Project_Room(driver)
        elif page_name == 'project_new_page':
            page_obj = Project_New(driver)
        elif page_name == 'gettyimage_page':
            page_obj = Getty_Image(driver)
        elif page_name == 'shape_designer_page':
            page_obj = Shape_Designer(driver)
        elif page_name == 'intro_video_room_page':
            page_obj = Intro_Video_Room(driver)
        elif page_name == 'crop_image_page':
            page_obj = Crop_Image(driver)
        elif page_name == 'subtitle_room_page':
            page_obj = Subtitle_Room(driver)
        elif page_name == 'audio_editing_page':
            page_obj = Audio_Editing(driver)
        elif page_name == 'motion_tracker_page':
            page_obj = Motion_Tracker(driver)
        elif page_name == 'effect_settings_page':
            page_obj = Effect_Settings(driver)
        else:
            logger(f'incorrect page_name : {page_name}')
            return None
        for name, fn in inspect.getmembers(page_obj, inspect.isfunction):
            if isinstance(fn, types.FunctionType) and name != 'deco':
                try:
                    setattr(page_obj, name, page_obj.deco(fn))
                except:
                    ...
        return page_obj


