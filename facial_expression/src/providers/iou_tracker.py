import numpy as np
import cv2
from src.utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)

class IOUTracker:
    def __init__(self, config):
        self.max_age = config['MAX_AGE']
        self.iou_threshold = config['IOU_THRESHOLD']
        self.next_id = 0
        self.tracks = []
        """Tracker can track multiple objects in a frame. Each object is represented by a dictionary with the following keys: id, bdbox, age, updated."""
        """for future implementation, we can make interval result match with track.id"""

    def __calculate_iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxB[3], boxB[3])

        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou

    def update(self, detections):
        updated_tracks = []  # Initialize empty list every frame
        dead_tracks = []

        # Reset updated flag for all existing tracks
        for track in self.tracks:
            track['updated'] = False

        # Match detections to existing tracks
        for det in detections:
            best_iou = 0
            best_track = None

            for track in self.tracks:
                iou = self.__calculate_iou(track['bdbox'], det['bdbox'])                
                if iou > best_iou and iou >= self.iou_threshold:
                    best_iou = iou                                                      # Update IOU to find best match in tracks list
                    best_track = track                                                  # Find if any track matched best with detection
                logger.debug(f"IOU of {track}: {iou}")

            if best_track:
                best_track['bdbox'] = det['bdbox']
                best_track['age'] = 0
                best_track['updated'] = True
                updated_tracks.append(best_track)
                logger.info(f"Track ID {best_track['id']}: updated with IOU {best_iou:.4f}")
            else:                                                                       # New bag from left does not match with any old one
                self.next_id += 1
                new_track = {
                    'id': self.next_id,
                    'bdbox': det['bdbox'],
                    'age': 0,
                    'updated': True
                }
                updated_tracks.append(new_track)
                logger.info(f"Track ID {new_track['id']}: birth")

        # Update ages of remaining tracks that are not detected
        for track in self.tracks:
            if not track['updated']:
                track['age'] += 1
                if track['age'] > self.max_age:
                    dead_tracks.append(track)
                    logger.info(f"Track ID {track['id']}: dead")
                else:
                    updated_tracks.append(track)
                    logger.info(f"Track ID {track['id']}: alive with age {track['age']}")

        # logger.debug(f"Dead tracks: {dead_tracks}")
        # logger.debug(f"Old tracks: {self.tracks}")
        self.tracks = updated_tracks                                                     # Update tracks for next frame update                              
        # logger.debug(f"Updated tracks: {self.tracks}")
        return dead_tracks