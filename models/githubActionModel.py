from __future__ import annotations
from typing import Dict, List, Literal, Optional, Union, Any
from pydantic import BaseModel, Field, ValidationError,model_validator, ConfigDict
from enum import Enum

# Enum Definitions for Branding and Shells
class BrandingColor(str, Enum):
    white = "white"
    black = "black"
    yellow = "yellow"
    blue = "blue"
    green = "green"
    orange = "orange"
    red = "red"
    purple = "purple"
    gray_dark = "gray-dark"

class BrandingIcon(str, Enum):
    activity = "activity"
    airplay = "airplay"
    alert_circle = "alert-circle"
    alert_octagon = "alert-octagon"
    alert_triangle = "alert-triangle"
    align_center = "align-center"
    align_justify = "align-justify"
    align_left = "align-left"
    align_right = "align-right"
    anchor = "anchor"
    aperture = "aperture"
    archive = "archive"
    arrow_down_circle = "arrow-down-circle"
    arrow_down_left = "arrow-down-left"
    arrow_down_right = "arrow-down-right"
    arrow_down = "arrow-down"
    arrow_left_circle = "arrow-left-circle"
    arrow_left = "arrow-left"
    arrow_right_circle = "arrow-right-circle"
    arrow_right = "arrow-right"
    arrow_up_circle = "arrow-up-circle"
    arrow_up_left = "arrow-up-left"
    arrow_up_right = "arrow-up-right"
    arrow_up = "arrow-up"
    at_sign = "at-sign"
    award = "award"
    bar_chart_2 = "bar-chart-2"
    bar_chart = "bar-chart"
    battery_charging = "battery-charging"
    battery = "battery"
    bell_off = "bell-off"
    bell = "bell"
    bluetooth = "bluetooth"
    bold = "bold"
    book_open = "book-open"
    book = "book"
    bookmark = "bookmark"
    box = "box"
    briefcase = "briefcase"
    calendar = "calendar"
    camera_off = "camera-off"
    camera = "camera"
    cast = "cast"
    check_circle = "check-circle"
    check_square = "check-square"
    check = "check"
    chevron_down = "chevron-down"
    chevron_left = "chevron-left"
    chevron_right = "chevron-right"
    chevron_up = "chevron-up"
    chevrons_down = "chevrons-down"
    chevrons_left = "chevrons-left"
    chevrons_right = "chevrons-right"
    chevrons_up = "chevrons-up"
    circle = "circle"
    clipboard = "clipboard"
    clock = "clock"
    cloud_drizzle = "cloud-drizzle"
    cloud_lightning = "cloud-lightning"
    cloud_off = "cloud-off"
    cloud_rain = "cloud-rain"
    cloud_snow = "cloud-snow"
    cloud = "cloud"
    code = "code"
    command = "command"
    compass = "compass"
    copy = "copy"
    corner_down_left = "corner-down-left"
    corner_down_right = "corner-down-right"
    corner_left_down = "corner-left-down"
    corner_left_up = "corner-left-up"
    corner_right_down = "corner-right-down"
    corner_right_up = "corner-right-up"
    corner_up_left = "corner-up-left"
    corner_up_right = "corner-up-right"
    cpu = "cpu"
    credit_card = "credit-card"
    crop = "crop"
    crosshair = "crosshair"
    database = "database"
    delete = "delete"
    disc = "disc"
    dollar_sign = "dollar-sign"
    download_cloud = "download-cloud"
    download = "download"
    droplet = "droplet"
    edit_2 = "edit-2"
    edit_3 = "edit-3"
    edit = "edit"
    external_link = "external-link"
    eye_off = "eye-off"
    eye = "eye"
    fast_forward = "fast-forward"
    feather = "feather"
    file_minus = "file-minus"
    file_plus = "file-plus"
    file_text = "file-text"
    file = "file"
    film = "film"
    filter = "filter"
    flag = "flag"
    folder_minus = "folder-minus"
    folder_plus = "folder-plus"
    folder = "folder"
    gift = "gift"
    git_branch = "git-branch"
    git_commit = "git-commit"
    git_merge = "git-merge"
    git_pull_request = "git-pull-request"
    globe = "globe"
    grid = "grid"
    hard_drive = "hard-drive"
    hash = "hash"
    headphones = "headphones"
    heart = "heart"
    help_circle = "help-circle"
    home = "home"
    image = "image"
    inbox = "inbox"
    info = "info"
    italic = "italic"
    layers = "layers"
    layout = "layout"
    life_buoy = "life-buoy"
    link_2 = "link-2"
    link = "link"
    list = "list"
    loader = "loader"
    lock = "lock"
    log_in = "log-in"
    log_out = "log-out"
    mail = "mail"
    map_pin = "map-pin"
    map = "map"
    maximize_2 = "maximize-2"
    maximize = "maximize"
    menu = "menu"
    message_circle = "message-circle"
    message_square = "message-square"
    mic_off = "mic-off"
    mic = "mic"
    minimize_2 = "minimize-2"
    minimize = "minimize"
    minus_circle = "minus-circle"
    minus_square = "minus-square"
    minus = "minus"
    monitor = "monitor"
    moon = "moon"
    more_horizontal = "more-horizontal"
    more_vertical = "more-vertical"
    move = "move"
    music = "music"
    navigation_2 = "navigation-2"
    navigation = "navigation"
    octagon = "octagon"
    package = "package"
    paperclip = "paperclip"
    pause_circle = "pause-circle"
    pause = "pause"
    percent = "percent"
    phone_call = "phone-call"
    phone_forwarded = "phone-forwarded"
    phone_incoming = "phone-incoming"
    phone_missed = "phone-missed"
    phone_off = "phone-off"
    phone_outgoing = "phone-outgoing"
    phone = "phone"
    pie_chart = "pie-chart"
    play_circle = "play-circle"
    play = "play"
    plus_circle = "plus-circle"
    plus_square = "plus-square"
    plus = "plus"
    pocket = "pocket"
    power = "power"
    printer = "printer"
    radio = "radio"
    refresh_ccw = "refresh-ccw"
    refresh_cw = "refresh-cw"
    repeat = "repeat"
    rewind = "rewind"
    rotate_ccw = "rotate-ccw"
    rotate_cw = "rotate-cw"
    rss = "rss"
    save = "save"
    scissors = "scissors"
    search = "search"
    send = "send"
    server = "server"
    settings = "settings"
    share_2 = "share-2"
    share = "share"
    shield_off = "shield-off"
    shield = "shield"
    shopping_bag = "shopping-bag"
    shopping_cart = "shopping-cart"
    shuffle = "shuffle"
    sidebar = "sidebar"
    skip_back = "skip-back"
    skip_forward = "skip-forward"
    slash = "slash"
    sliders = "sliders"
    smartphone = "smartphone"
    speaker = "speaker"
    square = "square"
    star = "star"
    stop_circle = "stop-circle"
    sun = "sun"
    sunrise = "sunrise"
    sunset = "sunset"
    table = "table"
    tablet = "tablet"
    tag = "tag"
    target = "target"
    terminal = "terminal"
    thermometer = "thermometer"
    thumbs_down = "thumbs-down"
    thumbs_up = "thumbs-up"
    toggle_left = "toggle-left"
    toggle_right = "toggle-right"
    trash_2 = "trash-2"
    trash = "trash"
    trending_down = "trending-down"
    trending_up = "trending-up"
    triangle = "triangle"
    truck = "truck"
    tv = "tv"
    type = "type"
    umbrella = "umbrella"
    underline = "underline"
    unlock = "unlock"
    upload_cloud = "upload-cloud"
    upload = "upload"
    user_check = "user-check"
    user_minus = "user-minus"
    user_plus = "user-plus"
    user_x = "user-x"
    user = "user"
    users = "users"
    video_off = "video-off"
    video = "video"
    voicemail = "voicemail"
    volume_1 = "volume-1"
    volume_2 = "volume-2"
    volume_x = "volume-x"
    volume = "volume"
    watch = "watch"
    wifi_off = "wifi-off"
    wifi = "wifi"
    wind = "wind"
    x_circle = "x-circle"
    x_square = "x-square"
    x = "x"
    zap_off = "zap-off"
    zap = "zap"
    zoom_in = "zoom-in"
    zoom_out = "zoom-out"

class Shell(str, Enum):
    bash = "bash"
    pwsh = "pwsh"
    python = "python"
    sh = "sh"
    cmd = "cmd"
    powershell = "powershell"

# Models for Inputs, Outputs, and Branding
class Input(BaseModel):
    description: str
    deprecationMessage: Optional[str] = None
    required: Optional[bool] = None
    default: Optional[str] = None

class Output(BaseModel):
    description: str

class CompositeOutput(Output):
    value: str

class Branding(BaseModel):
    color: BrandingColor
    icon: BrandingIcon

# Models for 'runs' variations
class RunsJavascript(BaseModel):
    using: Literal["node12", "node16", "node20"]
    main: str
    pre: Optional[str] = None
    pre_if: Optional[str] = Field(None, alias="pre-if")
    post: Optional[str] = None
    post_if: Optional[str] = Field(None, alias="post-if")

class CompositeStep(BaseModel):
    run: Optional[str] = None
    shell: Optional[Union[Shell, str]] = None
    uses: Optional[str] = None
    with_args: Optional[Dict[str, Any]] = Field(None, alias="with")
    name: Optional[str] = None
    id: Optional[str] = None
    if_conditional: Optional[str] = Field(None, alias="if")
    env: Optional[Dict[str, Union[str, int, bool]]] = None
    continue_on_error: Union[bool, str] = Field(False, alias="continue-on-error")
    working_directory: Optional[str] = Field(None, alias="working-directory")

    @model_validator(mode="before")
    def check_run_or_uses(cls, values):
        """Ensures that either 'run' and 'shell' are provided, or 'uses' is provided."""
        has_run = 'run' in values and 'shell' in values
        has_uses = 'uses' in values
        if not (has_run or has_uses):
            raise ValueError("A step must have either 'uses' or both 'run' and 'shell'")
        return values

class RunsComposite(BaseModel):
    using: Literal["composite"]
    steps: List[CompositeStep]

class RunsDocker(BaseModel):
    using: Literal["docker"]
    image: str
    env: Optional[Dict[str, Union[str, int, bool]]] = None
    entrypoint: Optional[str] = None
    pre_entrypoint: Optional[str] = Field(None, alias="pre-entrypoint")
    pre_if: Optional[str] = Field(None, alias="pre-if")
    post_entrypoint: Optional[str] = Field(None, alias="post-entrypoint")
    post_if: Optional[str] = Field(None, alias="post-if")
    args: Optional[List[str]] = None

class GitHubAction(BaseModel):
    """
    Pydantic model for GitHub Action metadata (action.yml).
    """
    name: str
    description: str
    runs: Union[RunsJavascript, RunsComposite, RunsDocker] = Field(..., discriminator="using")
    author: Optional[str] = None
    inputs: Optional[Dict[str, Input]] = None
    outputs: Optional[Dict[str, Union[CompositeOutput, Output]]] = None
    branding: Optional[Branding] = None

    # This is the modern Pydantic V2 configuration
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        populate_by_name=True, # Replaces allow_population_by_field_name
    )

    @model_validator(mode='after')
    def validate_outputs(self): # The argument is conventionally named 'self' now
        """
        Validates that the 'outputs' field matches the type required by the 'runs' configuration.
        - Composite actions must use CompositeOutput (with a 'value').
        - Other actions must use Output (without a 'value').
        """
        # --- FIX: Use attribute access (self.runs) instead of dictionary access (self.get('runs')) ---
        runs, outputs = self.runs, self.outputs
        
        if not runs or not outputs:
            return self

        is_composite = runs.using == 'composite'
        
        for key, output_val in outputs.items():
            # Check if output_val is a Pydantic model before accessing its fields
            if not isinstance(output_val, BaseModel):
                 continue

            if is_composite:
                # For composite actions, it MUST be a CompositeOutput with 'value' set.
                if not isinstance(output_val, CompositeOutput) or 'value' not in output_val.model_fields_set:
                    raise ValueError(f"Output '{key}' for composite action must be a CompositeOutput with a 'value' field.")
            else: # Docker or Javascript
                # For other actions, it must NOT have a 'value' field.
                if 'value' in output_val.model_fields_set:
                    raise ValueError(f"Output '{key}' for non-composite action must not have a 'value' field.")
        return self