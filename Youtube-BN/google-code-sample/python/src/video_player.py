"""A video player class."""

from .video_library import VideoLibrary
import random, re
class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        #below variable is an global variable 
        # which will be used as stack to keep track of the current video playing
        self.video_playing = {}
        #below dictionary will keep the playlists and their videos
        self.playLists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")
        vid = []
        for x in range(len(videos)):
            #below lines will strip out some of the strings from tags 
            tag = str(videos[x].tags)
            characters_to_remove = "()'',"
            for character in characters_to_remove:
                tag = tag.replace(character, "")
            #formats the videos and includes to the list    
            inc = f"{videos[x].title} ({videos[x].video_id}) [{tag}]"
            vid.append(inc)
        #using the sort function to sort the formating and output
        alphetic_order = sorted(vid)
        for i in alphetic_order:
            print(i)

    
    
    def play_video(self, video_id):
        """Plays a video"""

        videos = self._video_library.get_video(video_id)
        
        #if already a video playing stop and start the new one
        if (len(self.video_playing) > 0) and bool(videos):
            print(f"Stopping video: {self.video_playing.popitem()[0]}")
            print(f"Playing video: {videos.title}")
            self.video_playing[videos.title] = 'playing'
        #starts the video new and adds it to the playing dictionary with status of playing
        elif bool(videos):
            print(f"Playing video: {videos.title}")
            self.video_playing[videos.title] = 'playing'
        else:
            print('Cannot play video: Video does not exist')


    def stop_video(self):
        #checks if the global variable has any video playing 
        #if it is then it stops playing and removes from the dictionary
        if (len(self.video_playing) > 0):
            print(f"Stopping video: {self.video_playing.popitem()[0]}")
        else:
            print('Cannot stop video: No video is currently playing')

    def play_random_video(self):

        """Plays a random video from the video library."""

        allvideos = self._video_library.get_all_videos()
        alltitles = []
        #titles of all videos are inserted in a list
        for x in range(len(allvideos)):
            alltitles.append(allvideos[x].title)

        #this will choose a titles from the list
        randchoice = random.choice(alltitles)

        #below after some validation checks the random title is played and other video is stopped
        if (len(self.video_playing) > 0):
            print(f"Stopping video: {self.video_playing.popitem()[0]}")
            print(f"Playing video: {randchoice}")
            self.video_playing[randchoice] = 'playing'
        else:
            print(f"Playing video: {randchoice}")
            self.video_playing[randchoice] = 'playing'


    def pause_video(self):
        #here we extract the value and key in order to check the status of video
        #if it is playing, we pause otherwise we show message
        if bool(self.video_playing):
            val = list(self.video_playing.values()).pop()
            ky = list(self.video_playing.keys()).pop()
            if (val != 'pause'):
                print(f"Pausing video: {ky}")
                self.video_playing[ky] = 'pause'
            else:
                print(f'Video already paused: {ky}')
        else:
            print('Cannot pause video: No video is currently playing')

    def continue_video(self):
        """Resumes playing the current video."""
        
        #this is similar to previous example as we also extract the key and value from dictionary
        #to check the video status and change to 'playin' when continued
        if bool(self.video_playing):
            val = list(self.video_playing.values()).pop()
            ky = list(self.video_playing.keys()).pop()
            if (val == 'pause'):
                print(f"Continuing video: {ky}")
                self.video_playing[ky] = 'playing'
            else:
                print('Cannot continue video: Video is not paused')
        else:
            print('Cannot continue video: No video is currently playing')


    def show_playing(self):
        """Displays video currently playing."""
        #this is where we also do similar thing as previously done to check the process
        #we also get all the videos to extract the videos information to display to user
        if bool(self.video_playing):
            #item = self.video_playing
            val = list(self.video_playing.values()).pop()
            ky = list(self.video_playing.keys()).pop()
            #gets all the videos
            videos = self._video_library.get_all_videos()
            for i in range(len(videos)):
                #below four line removes the extra characters to strip the tags
                tag = str(videos[i].tags)
                characters_to_remove = "()'',"
                for character in characters_to_remove:
                    tag = tag.replace(character, "")
                #this check is to see whether the video is paused to playing
                if videos[i].title == ky and val == 'pause':
                    print(f'Currently playing: {videos[i].title} ({videos[i].video_id}) [{tag}] - PAUSED')
                elif videos[i].title == ky:
                    print(f'Currently playing: {videos[i].title} ({videos[i].video_id}) [{tag}]')
        else:
            print('No video is currently playing')


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        #this is where we use our second global dictionary to store the playlists and the videos within it
        #below line makes the playlist uppercase to compare with user input for validation
        ky = list(self.playLists.keys())
        ky = [each_string.upper() for each_string in ky]
        if playlist_name.isspace():
            print("Cannot create playlist: This playlist contains empty whitespaces")
        elif playlist_name.upper() in ky:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            #creates the playlists with the given name
            self.playLists[playlist_name] = []
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        #we do similar thing as before by retrieving the playlist keys and checking with the user input for validation
        #we add the video_id of the video to the list as a value, so it can be used to retrieve video information with get_video() function
        playlists = list(self.playLists.keys())
        playlists = [each_string.upper() for each_string in playlists]
        vid = self._video_library.get_video(video_id)
        if playlist_name.upper() not in playlists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif not bool(vid):
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            #below checks are done to check for case sensitivity of given and stored playlist
            # if it matches we add it to the playlist 
            for keys in self.playLists:
                if keys.upper() == playlist_name.upper():
                    if video_id not in self.playLists[keys]:
                        self.playLists[keys].append(vid.video_id)
                        print(f"Added video to {playlist_name}: {vid.title}")
                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")

    def show_all_playlists(self):
        
        """Display all playlists."""
        #below two lines gets the keys and sorts them in alphabetic order regardless of their case sensitivity
        playlists = list(self.playLists.keys())
        playlists = sorted(playlists, key=lambda k: (k.lower(), k.islower()))
        if len(playlists) <= 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists: ")
            for i in playlists:
                print(i)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        #below two lines will get all the playlist names and turn them into uppercase for comparison with playlist_name
        playlists = list(self.playLists.keys())
        playlists = [each_string.upper() for each_string in playlists]
        
        #this variable will be used as copy of the original global variable so that original dictionary does not get affected
        #the for loop will retrive all the playlist with keys being the uppercase and value being the original playlist name
        #the checks are done to avoid error of case sensitivity as the user may enter playlist name in different case
        local_playList = {}
        for key in self.playLists:
            local_playList[key.upper()] = self.playLists[key]
        if playlist_name.upper() in playlists:
            print(f"Showing playlist: {playlist_name}")
            if len(local_playList[playlist_name.upper()]) <= 0:
                print("No videos here yet")
            else:
                #below we are comparing and iterating through the playlist to find the video user looking for
                #multiple checks are done to handle if the user inputs different case string for their playlist names
                for keys in self.playLists:
                    if keys.upper() == playlist_name.upper():
                        for i in self.playLists[keys]:
                            vid = self._video_library.get_video(i)
                            #below three lines strips the tags
                            tag = str(vid.tags)
                            characters_to_remove = "()'',"
                            for character in characters_to_remove:
                                tag = tag.replace(character, "")
                            print(f'{vid.title} ({vid.video_id}) [{tag}]')
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlists = list(self.playLists.keys())
        playlists = [each_string.upper() for each_string in playlists]
        vid = self._video_library.get_video(video_id)
        if playlist_name.upper() not in playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        elif not bool(vid):
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            #if above checks do not apply we will do some checks by iterating through the playlist and finding the video
            #then check for case sensitivity then remove
            for keys in self.playLists:
                if keys.upper() == playlist_name.upper():
                    if video_id in self.playLists[keys]:
                        self.playLists[keys].remove(video_id)
                        print(f"Removed video from {playlist_name}: {vid.title}")
                    else:
                        print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):

        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlists = list(self.playLists.keys())
        playlists = [each_string.upper() for each_string in playlists]
        if playlist_name.upper() not in playlists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            #if above checks do not apply we will do some checks by iterating through the playlist and finding the video
            #then check for case sensitivity then clear the array of the given playlist
            for keys in self.playLists:
                if keys.upper() == playlist_name.upper():
                    self.playLists[keys].clear()
                    print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlists = list(self.playLists.keys())
        playlists = [each_string.upper() for each_string in playlists]
        if playlist_name.upper() not in playlists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            #we are transforming the playlist into list in order to avoid loop error as we will be deleting an dictionary element during the dictionary loop
            for keys in list(self.playLists):
                if keys.upper() == playlist_name.upper():
                    del self.playLists[keys]
                    print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        vid_tracker = []
        for x in range(len(videos)):
            if search_term.upper() in videos[x].title.upper():
                vid_tracker.append(videos[x].title)
        vid_tracker = sorted(vid_tracker)
        #print(vid_tracker)
        if len(vid_tracker) <= 0:
                print(f"No search results for {search_term}")
        else:
            print("Here are the results for cat:")
            for i in range(len(vid_tracker)):
                for k in range(len(videos)):
                    if videos[k].title == vid_tracker[i]:
                        tag = str(videos[k].tags)
                        characters_to_remove = "()'',"
                        for character in characters_to_remove:
                            tag = tag.replace(character, "")
                        print(f"{i+1}) {videos[k].title} ({videos[k].video_id}) [{tag}] ")
        print("Would you like to play any of the above? If yes, specify the number of the video. \n If your answer is not a valid number, we will assume it's a no.")
        choice = input()
        for i in range(len(vid_tracker)):
            if choice.isdigit():
                if int(choice) == i+1:
                    print(f"Playing video: {vid_tracker[i]}")
                    self.video_playing[vid_tracker[i]] = 'playing'


        def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        vid_tracker = []
        for x in range(len(videos)):
            if search_term.upper() in videos[x].title.upper():
                vid_tracker.append(videos[x].title)
        vid_tracker = sorted(vid_tracker)
        #print(vid_tracker)
        if len(vid_tracker) <= 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i in range(len(vid_tracker)):
                for k in range(len(videos)):
                    if videos[k].title == vid_tracker[i]:
                        tag = str(videos[k].tags)
                        characters_to_remove = "()'',"
                        for character in characters_to_remove:
                            tag = tag.replace(character, "")
                        print(f"{i+1}) {videos[k].title} ({videos[k].video_id}) [{tag}] ")
            print("Would you like to play any of the above? If yes, specify the number of the video. \n If your answer is not a valid number, we will assume it's a no.")
            choice = input()
            for i in range(len(vid_tracker)):
                if choice.isdigit():
                    if int(choice) == i+1:
                        print(f"Playing video: {vid_tracker[i]}")
                        self.video_playing[vid_tracker[i]] = 'playing'


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        tag_tracker = []
        for x in range(len(videos)):
            check = list(videos[x].tags)
            out = map(lambda x:x.upper(), check)
            output = list(out)
            if video_tag.upper() in output:
                tag_tracker.append(videos[x].title)
        vid_tracker = sorted(tag_tracker)
        if len(vid_tracker) <= 0:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(vid_tracker)):
                for k in range(len(videos)):
                    if videos[k].title == vid_tracker[i]:
                        tag = str(videos[k].tags)
                        characters_to_remove = "()'',"
                        for character in characters_to_remove:
                            tag = tag.replace(character, "")
                        print(f"{i+1}) {videos[k].title} ({videos[k].video_id}) [{tag}] ")
            print("Would you like to play any of the above? If yes, specify the number of the video. \n If your answer is not a valid number, we will assume it's a no.")
            choice = input()
            for i in range(len(vid_tracker)):
                if choice.isdigit():
                    if int(choice) == i+1:
                        print(f"Playing video: {vid_tracker[i]}")
                        self.video_playing[vid_tracker[i]] = 'playing'
