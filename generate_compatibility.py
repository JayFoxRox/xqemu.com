#!/bin/env python3

import html
import os
import csv
from urllib.request import urlopen
from urllib.request import Request
import sys
import json
import datetime


# Helper function to get compatibility list (John GodGames Google sheet)
def GetXQEMUCompatibilityList():
    sheet = "1sVtQ9SNPathKAMCqfYtvJQP0bs0UeLzP9otPHvZDMwE"
    url = "https://docs.google.com/spreadsheets/d/%s/export?format=csv" % sheet

    games = []

    page_req = Request(url, headers={'User-Agent' : "XQEMU-Compatibility"}) 
    page_res = urlopen(url)
    page_data = page_res.read()

    page_data = page_data.decode("utf-8")
    #print(page_data)

    values = [x for x in csv.reader(page_data.split('\n'))]

    heads = []
    for i, row in enumerate(values):            
        
      # Some rows might be to short, so we extend them
      row += [''] * max(0, len(heads) - len(row))

      # Parse the header
      if i == 0:
        for h in row:
          name = h.strip()
          if name == "": break
          if name == "Repo.": name = "Repository"
          if name == "commit": name = "Commit"
          heads += [name]
        continue

      # Parse each row
      test = {}
      for j in range(len(heads)):
        test[heads[j]] = row[j].strip()

      # Game probably wasn't tested if this condition is true
      if (test['Status'] == "" and test['Broken'] == ""):
        continue

      games += [test]

    return games

commit_cache = {}
def GetCommitInformation(user, repository, commit): 
  global commit_cache

  # Create a cache key
  key = (user.lower(), repository.lower(), commit.lower())

  # Do cache lookup
  if key in commit_cache:
    return commit_cache[key]

  # Construct the GitHub URL
  url = "https://api.github.com/repos/%s/%s/git/commits/%s" % (key[0], key[1], key[2])

  # Request data
  page_req = Request(url, headers={'User-Agent' : "XQEMU-Compatibility"}) 
  page_res = urlopen(url)
  page_data = page_res.read()

  # Parse JSON object
  value = json.loads(page_data)

  # Fill cache and return
  commit_cache[key] = value
  return value


# Get compatibility list
xqemu_compatibility = GetXQEMUCompatibilityList()

# Sort list by name
#FIXME: Add row information first, so we can trace info back to source
#FIXME: Make 'Æ' [from "Æon Flux"] equivalent to "Ae"
xqemu_compatibility = sorted(xqemu_compatibility, key=lambda k: k['Title']) 





s = 'title: Compatibility List\n'

s += '!!! attention\n\tThis article is auto generated\n\n'

if False:
  s += '<script src="https://www.w3schools.com/lib/w3.js"></script>'

  s += '<script>function filter_function(e) {' \
          'var s = document.getElementById("filter_text");' \
          'w3.filterHTML(\'#compatibility_table\', \'.item\', s.value);' \
          'e.stopPropagation();' \
       '}</script>'

  s += '<input type="text" id="filter_text" onkeydown="event.stopPropagation()" onkeyup="filter_function(event)" placeholder="Filter names.." style="width:100%;">'


# Our theme doesn't want 100% table width, even if we request it (inline-block)
# We can work around it using block display
s += '<style>.md-typeset__table { display:block !important; }</style>\n'

s += '<table id="compatibility_table" style="width:100%">\n'
s += '<tr><th></th><th width="50%" onclick="w3.sortHTML(\'#compatibility_table\', \'.item\', \'td:nth-child(2)\')" style="cursor:pointer">Game title</th><th width="30%">Status</th></tr>'
row = 0
for report in xqemu_compatibility:
  row += 1


  #FIXME: This is a bit weird..
  if report['Title'] == '':
    continue


  def flag(s):
    r = ""
    for c in s.lower():
      r += "&#x%X;" % (0x1f1e6 + ord(c) - ord('a'))
    return r

  regions = [
    "&#x1F310;", # world (should only be used alone?)
    flag("au"), # australia
    flag("eu"), # european union
    flag("jp"), # japan
    flag("us"), # united states
    flag("de"), # germany
    flag("fr"), # france
    flag("es"), # spain
    flag("it"), # italy
    flag("at"), # austria
    flag("ch") # switzerland
  ]
  region = []
  for i in range(1 + row % 3):
    region += [regions[(row + i) % len(regions)]]
  title_id = 'XQ-%03d<br>Release: 1.00 ( %s )' % (row, " ".join(region))
  title_id += '<br><br><br><span style="color:gray;">Filename: D:\\default.xbe<br>Timestamp: 0x12345678</span>'
  status_types = {
    'Ingame': 'orange', # Can go ingame
    'Menu': 'black', # Menu shows up
    'Intro': 'black', # Intro animations / logos play
    'Nothing': 'gray', # Not even intro can be seen
    'Untested': 'lightgray' # Untested
  }
  exit_reasons = [
    None, # Emulation did not stop / no reason to exit
    'Stuck', # Xbox waits / repeats same step or simply can't continue
    'Hangs', # PC is busy and never returns to emulation
    'Crashes', # Unexpected stop
    'Aborts' # Forced stop [assert etc.]
  ]
  covers = {
    '187 Ride or Die': 'https://www.mobygames.com/images/covers/l/173611-187-ride-or-die-xbox-front-cover.png',
    '007: Everything or Nothing': 'https://images-na.ssl-images-amazon.com/images/I/51RDG50EJVL._SY445_.jpg',
    'Egg Mania: Eggstreme Madness': 'https://gamefaqs.akamaized.net/box/5/9/9/17599_front.jpg',
    'Alias': 'https://images-na.ssl-images-amazon.com/images/I/411J6WCQYSL._SY445_.jpg',
    'Amped: Freestyle Snowboarding': 'https://www.mobygames.com/images/covers/l/84755-amped-freestyle-snowboarding-xbox-front-cover.jpg',
    'Amped 2': 'https://upload.wikimedia.org/wikipedia/en/thumb/2/2c/Amped_2_Coverart.png/220px-Amped_2_Coverart.png',
    'Barbie Horse Adventures: Wild Horse Rescue': 'https://www.mobygames.com/images/covers/l/145024-barbie-horse-adventures-wild-horse-rescue-xbox-front-cover.jpg',
    'Dead or Alive 3': 'https://www.mobygames.com/images/covers/l/84761-dead-or-alive-3-xbox-front-cover.jpg',
    'Dead or Alive Ultimate': 'https://www.mobygames.com/images/covers/l/48859-dead-or-alive-ultimate-xbox-front-cover.jpg',
    'Dead or Alive Xtreme Beach Volleyball': 'https://www.mobygames.com/images/covers/l/36112-dead-or-alive-xtreme-beach-volleyball-xbox-front-cover.jpg',
    'Sega GT 2002': 'https://www.mobygames.com/images/covers/l/19904-sega-gt-2002-xbox-front-cover.jpg',
    'Jet Set Radio Future': 'https://www.mobygames.com/images/covers/l/120463-jsrf-jet-set-radio-future-xbox-front-cover.jpg',
    'Project Gotham Racing': 'https://upload.wikimedia.org/wikipedia/en/thumb/6/6e/Project_Gotham_Racing_Coverart.png/220px-Project_Gotham_Racing_Coverart.png',
    'Project Gotham Racing 2': 'https://images-na.ssl-images-amazon.com/images/I/51fLfVbvm7L._AC_SX215_.jpg',
    'Batman: Rise of Sin Tzu': 'https://images-na.ssl-images-amazon.com/images/I/51JYAMMHumL._SY445_.jpg',
    'Crash Bandicoot: The Wrath of Cortex': 'https://images-na.ssl-images-amazon.com/images/I/51NoZe5iQbL.AC_SX215_.jpg',
    'Crash Nitro Kart': 'https://images-na.ssl-images-amazon.com/images/I/51168RGG8TL._SY445_.jpg',
    'Crazy Taxi 3: High Roller': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e9/Crazy_Taxi_3_-_High_Roller_Coverart.png/220px-Crazy_Taxi_3_-_High_Roller_Coverart.png',
    'Corvette': 'https://www.mobygames.com/images/covers/l/172885-corvette-xbox-front-cover.png',
    'Conker: Live & Reloaded': 'https://videogame-wizards.com/wp-content/uploads/2018/01/conkers-live-reloaded.jpg',
    'The Simpsons: Hit & Run': 'http://xboxaddict.com/images/box_art/628.jpg',
    'Crash Tag Team Racing': 'https://images-na.ssl-images-amazon.com/images/I/51R47DKDKGL.AC_SX215_.jpg',
    'Grand Theft Auto III': 'https://www.mobygames.com/images/covers/l/26921-rockstar-games-double-pack-grand-theft-auto-xbox-inside-cover.jpg',
    'Grand Theft Auto: Vice City': 'https://www.mobygames.com/images/covers/l/26922-rockstar-games-double-pack-grand-theft-auto-xbox-inside-cover.jpg',
    'Grand Theft Auto: San Andreas': 'https://www.mobygames.com/images/covers/l/65523-grand-theft-auto-san-andreas-xbox-front-cover.jpg',
    'Halo 2': 'https://www.mobygames.com/images/covers/l/38333-halo-2-xbox-front-cover.jpg',
    'Halo: Combat Evolved': 'https://vignette.wikia.nocookie.net/halo/images/8/81/Halo_Combat_Evolved_-_Xbox_Cover.png/revision/latest/scale-to-width-down/334?cb=20150331162657',
    'Hot Wheels: Stunt Track Challenge': 'https://www.lukiegames.com/assets/images/XBOX/xbox_hot_wheels_stunt_track_challenge-110214.jpg',
    'Burnout 2 (Developer\'s Cut)': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQq-EhuCr5Yzby_M-vJSbcmQMbINI1JKwceSdS5XLUPT8an8IKqKQ',
    'Tony Hawk\'s Pro Skater 2x': 'https://www.mobygames.com/images/covers/l/12211-tony-hawk-s-pro-skater-2x-xbox-front-cover.jpg',
    'Tony Hawk\'s Pro Skater 3': 'https://www.mobygames.com/images/covers/l/511585-tony-hawk-s-pro-skater-3-xbox-front-cover.jpg',
    'Tony Hawk\'s Pro Skater 4': 'https://www.mobygames.com/images/covers/l/15666-tony-hawk-s-pro-skater-4-xbox-front-cover.jpg',
    'Tony Hawk\'s Underground': 'https://www.mobygames.com/images/covers/l/26593-tony-hawk-s-underground-xbox-front-cover.jpg',
    'Tony Hawk\'s Underground 2': 'https://www.mobygames.com/images/covers/l/50495-tony-hawk-s-underground-2-xbox-front-cover.jpg',
    'Tony Hawk\'s American Wasteland': 'https://www.mobygames.com/images/covers/l/63107-tony-hawk-s-american-wasteland-xbox-front-cover.jpg',
    'Tony Hawk\'s Project 8': 'https://www.mobygames.com/images/covers/l/180433-tony-hawk-s-project-8-xbox-front-cover.png',
    'Midtown Madness 3': 'https://www.mobygames.com/images/covers/l/28406-midtown-madness-3-xbox-front-cover.jpg',
    'Metal Slug 3': 'https://www.mobygames.com/images/covers/l/76678-metal-slug-3-xbox-front-cover.jpg',
    'Metal Slug 4': 'https://images-na.ssl-images-amazon.com/images/I/51PDYS5EQTL._SY445_.jpg',
    'Metal Slug 5': 'https://vignette.wikia.nocookie.net/metalslug/images/d/d9/Metal_Slug_5_Xbox_Cover.jpg',
    'Mashed: Drive to Survive': 'http://xboxaddict.com/images/box_art/4298.jpg',
    'Mashed: Fully Loaded': 'https://images-na.ssl-images-amazon.com/images/I/512KWAXKC2L._SY445_.jpg',
    'MotoGP': 'https://www.mobygames.com/images/covers/l/223734-motogp-ultimate-racing-technology-xbox-front-cover.png',
    'MotoGP 2': 'https://www.mobygames.com/images/covers/l/37739-motogp-2-xbox-front-cover.jpg',
    'MotoGP 3': 'https://www.mobygames.com/images/covers/l/190031-motogp-ultimate-racing-technology-3-xbox-front-cover.png',
    'Ninja Gaiden': 'https://cashinculture.3dcartstores.com/assets/images/Ninja%20Gaiden%20xbo.jpg',
    'Ninja Gaiden Black': 'https://www.mobygames.com/images/covers/l/63727-ninja-gaiden-black-xbox-front-cover.jpg',
    'OutRun 2': 'https://www.mobygames.com/images/covers/l/190011-outrun-2-xbox-front-cover.jpg',
    'OutRun 2006: Coast 2 Coast': 'https://www.mobygames.com/images/covers/l/118456-outrun-2006-coast-2-coast-xbox-front-cover.jpg',
    'Outlaw Golf 2': 'https://www.mobygames.com/images/covers/l/77982-outlaw-golf-2-xbox-front-cover.jpg',
    'Outlaw Volleyball': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/ab/Outlaw_Volleyball_Coverart.png/220px-Outlaw_Volleyball_Coverart.png',
    'Pure Pinball': 'https://www.lukiegames.com/assets/images/XBOX/xbox_pure_pinball-110214.jpg',
    'RollerCoaster Tycoon': 'https://images-na.ssl-images-amazon.com/images/I/513YGWYJR5L._SY445_.jpg',
    'Kung Fu Chaos': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/ab/Kung_Fu_Chaos.jpg/220px-Kung_Fu_Chaos.jpg',
    'Counter-Strike': 'https://images-na.ssl-images-amazon.com/images/I/517P1V6XNQL._AC_SX215_.jpg',
    'Mechassault': 'https://www.mobygames.com/images/covers/l/38621-mechassault-xbox-front-cover.jpg',
    'Fuzion Frenzy': 'https://cdn4.spong.com/pack/f/u/fuzionfren54194/_-Fuzion-Frenzy-Xbox-_.jpg',
    'Burnout 3: Takedown': 'https://www.mobygames.com/images/covers/l/194942-burnout-3-takedown-xbox-front-cover.png',
    'Shenmue II': 'https://cdn3.spong.com/pack/s/h/shenmue291673/_-Shenmue-2-Xbox-_.jpg',
    'Star Wars: Battlefront': 'https://www.mobygames.com/images/covers/l/47712-star-wars-battlefront-xbox-front-cover.jpg',
    'Gunvalkyrie': 'https://www.mobygames.com/images/covers/l/216954-gunvalkyrie-xbox-front-cover.jpg',
    'Lego Star Wars II': 'https://www.mobygames.com/images/covers/l/190230-lego-star-wars-ii-the-original-trilogy-xbox-front-cover.png',
    'Crash Twinsanity': 'https://cdn1.spong.com/pack/c/r/crashtwins148671l/_-Crash-Twinsanity-Xbox-_.jpg',
    'Oddworld: Stranger\'s Wrath': 'https://www.mobygames.com/images/covers/l/128472-oddworld-stranger-s-wrath-xbox-front-cover.jpg',
    'Half-Life 2': 'https://www.mobygames.com/images/covers/l/184078-half-life-2-xbox-front-cover.jpg',
    'Harry Potter and the Chamber of Secrets': 'https://www.mobygames.com/images/covers/l/152397-harry-potter-and-the-chamber-of-secrets-xbox-front-cover.png',
    'Ultimate Pro Pinball': 'https://www.mobygames.com/images/covers/l/183523-pro-pinball-trilogy-xbox-front-cover.jpg',

    # Shrek is love, Shrek is life.
    'Shrek': 'https://upload.wikimedia.org/wikipedia/en/thumb/d/d9/Shrek_Coverart.png/220px-Shrek_Coverart.png',
    'Shrek 2': 'https://images-na.ssl-images-amazon.com/images/I/51uI5ZNvyCL.jpg',
    'Shrek SuperSlam': 'https://i.ebayimg.com/10/!!e!VNwgCGM~$(KGrHqV,!lMEz+4(R+8CBNP4L8o++Q~~_62.JPG',
    'Shrek Super Party': 'https://images-na.ssl-images-amazon.com/images/I/51B8uzSFchL._SY445_.jpg',
  }

  broken = report['Broken'].lower()

  notes = report['Notes'].lower()

  # Skip incomplete tests
  incomplete_test = False
  if broken == 'test':
    incomplete_test = True
  if report['Status'] == '':
    incomplete_test = True
  if report['Commit'] == '':
    incomplete_test = True

  if incomplete_test:
    version = None
    version_url = None
    version_date = None
    status_type = 'Untested'
  else:
    version = report['Commit'][0:8]
    version_url = "https://www.github.com/%s/%s/commits/%s" % (report['Author'], report['Repository'], report['Commit'])
    version_url = version_url.lower()
    version_date = GetCommitInformation(report['Author'], report['Repository'], report['Commit'])
    version_date = datetime.datetime.strptime(version_date['committer']['date'], '%Y-%m-%dT%H:%M:%SZ')
    version_date = "%04d-%02d-%02d" % (version_date.year,  version_date.month,  version_date.day)

    #FIXME: Remove this hack
    #  version += notes

    status_type = report['Status']

  # Fix some bugs in the sheet, where spelling is different
  status_type = status_type[0].upper() + status_type[1:].lower()

  #FIXME: What did the star mean?
  if status_type == 'Playable*':
    status_type = 'Playable'

  # "Playable" and "Ingame" are the same in the new format
  if status_type == 'Playable':
    status_type = 'Ingame'

  # Find color for the given status
  if status_type in status_types:
    status_color = status_types[status_type]
  else:
    print(status_type)
    assert(False)


  # These are actual output
  issue_type = []
  row_style = ''
  if not incomplete_test:

    # Collect all issues
    issue_types = []

    # Check for graphical issues
    graphics_issues = False
    if notes.find('lighting issues') != -1:
      graphics_issues = True
    if notes.find('broken characters') != -1:
      graphics_issues = True
    if notes.find('graphical bugs') != -1:
      graphics_issues = True
    if broken == 'lighting':
      graphics_issues = True

    # List graphical issues as problem
    if graphics_issues:
      issue_types += [('Broken graphics', 'Graphics emulation has issues')]

    # Always assume missing audio
    issue_types += [('Missing audio', "There is no audio emulation")]

    #FIXME: This should never happen anymore
    if notes.find('controls') != -1:
      issue_types += [('Broken input', "Notes: %s" % notes)]

    # Performance flag (Always assume slow)
    issue_types += [('Slow',"Performance assumption")]

    # Make issue list sexy
    for i, j in issue_types:
      issue_type += ['&#9888;&nbsp;<a style="color:black;" href="#" title="%s">%s</a>' % (j, i)]

    # Try to find the real exit reason
    if broken == '':
      exit_reason = None
    elif broken == 'lighting':
      exit_reason = ''
    elif broken == 'shader':
      exit_reason = 'Aborts'
    elif broken == 'texture':
      exit_reason = 'Aborts'
    elif broken[0:8] == 'hw/xbox/':
      exit_reason = 'Aborts'
    elif broken == 'noboot':
      exit_reason = 'Stuck'
    elif broken == 'performance':
      exit_reason = 'Stuck'
    elif broken == 'audio':
      exit_reason = None #FIXME: Is this okish?
    elif broken == 'memleak':
      exit_reason = 'Leaks memory'
    elif broken == 'crash':
      exit_reason = 'Crashes'
    else:
      assert(False)

    # Search notes for exit reason
    if exit_reason == None:
      if notes.find('hang') != -1:
        exit_reason = 'Stuck'
      if notes.find('stays at') != -1:
        exit_reason = 'Stuck'
      if notes.find('black screen') != -1:
        exit_reason = 'Stuck'

    # Append the exit reason
    if exit_reason != None:
      issue_type += ['&#x1F5D9;&nbsp;%s' % exit_reason]

    # Move to playable, if ingame and no exit-reason exists
    if exit_reason == None and status_type == 'Ingame':
      status_type = 'Playable'
      status_color = 'green'
      row_style = 'background: #EFFFD0;'
    elif status_type == 'Ingame':
      row_style = 'background: #FFFFE0;'

  #issue_type = [""] # ["&#x2714; No issues"]
  status = '<b style="color:%s">%s</b><br>%s' % (status_color, status_type, "<br>".join(issue_type))

  status += '<br><br><span style="color:gray;">'
  if version != None:
    assert(version_url != None) #FIXME: Don't add version_url if it's `None`
    status += 'Version:&nbsp;<a href=%s title="See recent changes for this version" style="color:gray; border-bottom:1px dotted gray;">%s</a>' % (version_url, version)
  if version_date != None:
    status += '<br>Version&nbsp;date:&nbsp;%s' % (version_date)
  status += '</span>'

  # Get the title
  game_title = report['Title']

  # Find the cover for this title
  if game_title in covers:
    cover = covers[game_title]
  else:
    #FIXME: Fallback cover
    cover = 'http://www.geldfritz.net/cdn/21/2002/861/xbox-360-game-cover-blank_136928.jpg' #list(covers.values())[row % len(covers)]

  s += '<tr class="item" style="%s">' % row_style
  s +=   '<td>'
  s +=     '<img style="height: 128px; border:1px solid gray; text-align: center;" src="%s" />' % cover
  s +=   '</td><td>'
  s +=     '<b class="name">%s</b><br>' % (html.escape(game_title))
  #s +=     'Title-ID: %s' % (title_id)
  s +=   '</td><td>'
  s +=     '%s' % (status)
  s +=   '</td>'
  s += '</tr>\n'

s += '</table>\n'

with open('docs/compatibility.md', 'wb') as f:
  f.write(s.encode('utf-8'))
