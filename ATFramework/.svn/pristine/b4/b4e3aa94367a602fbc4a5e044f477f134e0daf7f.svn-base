from pymediainfo import MediaInfo

# ==================================================================================================================
# Description: Retrieve the media info of the audio/video file
# Note: n/a
# Author: Jim Huang
# ==================================================================================================================


def parse_media_info(file_path):
    try:
        media_info = MediaInfo.parse(file_path)

        dict_result = {}
        for track in media_info.tracks:
            if track.track_type == 'General':
                print('enter General type')
                dict_result['format'] = track.format
                dict_result['file_size'] = track.file_size
                dict_result['duration'] = track.duration
            if track.track_type == 'Video':
                print('enter Video type')
                dict_result['width'] = track.width
                dict_result['height'] = track.height
                dict_result['resolution'] = str(track.width) + 'x' + str(track.height)
                dict_result['codec'] = track.codec
                dict_result['aspect_ratio'] = track.display_aspect_ratio
                dict_result['frame_rate'] = track.frame_rate
                dict_result['color_space'] = track.color_space
                dict_result['bit_depth'] = track.bit_depth
                dict_result['bit_rate'] = track.bit_rate
            if track.track_type == 'Audio':
                print('enter Audio type')
                print(f'Audio Data: {track.to_data()}')
                dict_result['codec'] = track.format
                dict_result['bit_rate'] = track.bit_rate
                dict_result['bit_rate_mode'] = track.bit_rate_mode
                dict_result['sample_rate'] = track.sampling_rate
                dict_result['channels'] = track.channel_s
    except Exception as e:
        print(f'Exception occurs. Error={e}')
    return dict_result