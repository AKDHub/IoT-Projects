import requests
from datetime import datetime

# Base API url
BASE_API = "http://api.sr.se/api/v2"
# General parameters
FORMAT = "format=json"


class RadioProgram:
    """
    Defines a Swedish Radio Program object with attributes from SR API.
    """
    def __init__(self, program_id):
        api_endpoint = f"{BASE_API}/programs/{program_id}?{FORMAT}"
        response_json = requests.get(api_endpoint).json()['program']
        self.title = response_json['name']
        self.id = response_json['id']
        self.description = response_json['description']
        self.prg_url = response_json['programurl']
        self.img_url = response_json['programimage']

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_prg_url(self):
        return self.prg_url

    def get_img_url(self):
        return self.img_url


class ProgramEpisode:
    """
    Defines a Swedish Radio Program Episode with attributes from SR API.
    """
    def __init__(self, episode_id: int):
        api_endpoint = f"{BASE_API}/episodes/get?id={episode_id}&{FORMAT}"
        response_json = requests.get(api_endpoint).json()['episode']
        # print(response_json)
        self.title = response_json['title']
        self.description = response_json['description']
        self.url = response_json['url']
        self.img_url = response_json['imageurl']
        self.text = ""
        if "text" in response_json:
            self.text = response_json['text']

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_url(self):
        return self.url

    def get_img_url(self):
        return self.img_url

    def get_text(self):
        return self.text


class RadioScheduleEntry:
    """
    Defines a Schedule Entry in a Swedish Radio Channel Schedule.
    """
    def __init__(self, schedule_entry):
        self.title = schedule_entry['title']

        self.description = ""
        if "description" in schedule_entry:
            self.description = schedule_entry['description']

        self.image_url = ""
        if "imageurl" in schedule_entry:
            self.image_url = schedule_entry['imageurl']

        self.prg_id = schedule_entry['program']['id']

        self.episode_id = 0
        if "episodeid" in schedule_entry:
            self.episode_id = schedule_entry['episodeid']

        self.start_time = convert_to_datetime(schedule_entry['starttimeutc'])
        self.end_time = convert_to_datetime(schedule_entry['endtimeutc'])

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_image_url(self):
        return self.image_url

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_image_data(self):
        """
        Returns image data if available.
        :return:
        """
        if self.image_url != "":
            return get_img_data_from_url(self.image_url)
        else:
            return False

    def get_prg_id(self):
        return self.prg_id

    def get_episode_id(self):
        return self.episode_id

    def __str__(self):
        ret_str = "%s - %s" % (self.get_start_time().strftime('%H:%M'), self.get_title())
        return ret_str


class RadioChannel:
    """
    Defines a Swedish Radio Channel and its attributes from SR API
    """
    def __init__(self, channel):
        self.name = channel["name"]
        self.img_url = ""
        if "image" in channel:
            self.img_url = channel["image"]
        self.tagline = channel["tagline"]
        self.liveaudio = channel["liveaudio"]["url"]
        self.schedule_entries = self.get_schedule_entries(self.get_schedule_url(channel))

    def __str__(self):
        """
        Return Channel object as String.
        :return:
        """
        ret_str = f"""
        Channel 
            name: {self.name}
            picture: {self.img_url}
            taglinge: {self.tagline}
            liveaudio: {self.liveaudio}
            Schedule:
"""
        for entry in self.get_schedule_from_now():
            ret_str += f"\t\t\t\t{entry.get_start_time()}, {entry.get_title()}\n"
        ret_str += "\n\n"
        return ret_str

    def get_name(self):
        return self.name

    def get_picture_url(self):
        return self.img_url

    def get_tagline(self):
        return self.tagline

    def get_liveaudio_url(self):
        return self.liveaudio

    def get_image_data(self):
        """
        Returns image data if available.
        :return:
        """
        if self.img_url != "":
            return get_img_data_from_url(self.img_url)
        else:
            return False

    def get_schedule_entries(self):
        return self.schedule_entries

    def get_schedule_from_now(self):
        """
        Gets all entries starting from current time including current playing program.
        :return:
        """
        sched_from_now = []
        for entry in self.schedule_entries:
            if ((entry.get_start_time() > datetime.now()) or
                    (entry.get_start_time() < datetime.now() < entry.get_end_time())):
                sched_from_now.append(entry)
        return sched_from_now

    def get_schedule_url(self, channel):
        """
        Builds and returns a string to request Channel Schedule from SR API.
        :param channel:
        :return:
        """
        # Build schedule URL with channel id and other parameters.
        # print(f"Channel: {channel['name']} id: {channel['id']}")
        base_str = f"{BASE_API}/scheduledepisodes"
        channel_id_str = f"channelid={channel['id']}"
        fromdate_str = f"fromdate={datetime.today().strftime('%Y-%m-%d')}"
        todate_str = f"todate={datetime.today().strftime('%Y-%m-%d')}"
        format_str = f"{FORMAT}"
        size_str = "size=200"
        return f"{base_str}?{channel_id_str}&{fromdate_str}&{fromdate_str}&{todate_str}&{format_str}&{size_str}"

    def get_schedule_entries(self, schedule_url) -> list:
        """
        Gets Radio Channel Schedule from SR API using schedule_url.
        Returns list of schedule entries.
        :param schedule_url:
        :return:
        """
        schedule_entries = []
        #print(schedule_url)
        try:
            response = requests.get(schedule_url)
            #print(response.content)
        except requests.ConnectionError as e:
            print(e)

        if is_successful(response.status_code):
            for entry in response.json()["schedule"]:
                schedule_entries.append(RadioScheduleEntry(entry))
                #print(entry)
        return schedule_entries

    def get_current_prg(self):
        """
        Returns current playing program on the Channel.
        :return:
        """
        return self.get_schedule_from_now()[0]


class SwedishRadioStation:
    """
    Defines a Swedish Radio Station with all its Channels available thru SR API.
    """
    def __init__(self, api_url):
        self.channels = []
        self.get_channels(api_url)

    def get_channels(self, api_url):
        """
        Gets all available channels from SR API url.
        :param api_url:
        :return:
        """
        response = requests.get(api_url)

        for channel in response.json()["channels"]:
            # print(channel)
            chanl = RadioChannel(channel)
            # print(chanl)
            self.channels.append(chanl)

    def __str__(self):
        ret_str = ""
        for channel in self.channels:
            ret_str += channel.__str__()
        return ret_str


# Helper functions
def convert_to_datetime(time):
    """
    Added as a result of a bug in SR API.
    Parses string and converts content to regular datetime object and returns it.
    """
    return datetime.utcfromtimestamp(int(time.strip("/Date()")[:-3]) + 3600)


def get_img_data_from_url(img_url):
    """
    Requests image data from image url.
    :param img_url:
    :return:
    """
    return requests.get(img_url).content


def is_successful(status_code: int) -> bool:
    """
    Checks if status code is a successful code. (200-299)
    :param status_code:
    :return:
    """
    if 200 <= status_code <= 299:
        return True
    else:
        return False


if __name__ == '__main__':
    sr_station = SwedishRadioStation(f"{BASE_API}/channels?{FORMAT}&size=49")
    print(sr_station)
    #prg = RadioProgram(program_id=2946)
    #episode = ProgramEpisode(episode_id=2283999)
