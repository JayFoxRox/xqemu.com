#!/bin/env python3

import html

s = 'title: Compatibility List\n'

s += '!!! attention\n\tThis article is auto generated\n\n'

s += '<script src="https://www.w3schools.com/lib/w3.js"></script>'

s += '<script>function filter_function(e) {' \
        'var s = document.getElementById("filter_text");' \
        'w3.filterHTML(\'#compatibility_table\', \'.item\', s.value);' \
        'e.stopPropagation();' \
     '}</script>'


# Our theme doesn't want 100% table width, even if we request it (inline-block)
# We can work around it using block display
s += '<style>.md-typeset__table { display:block !important; }</style>\n'



s += '<input type="text" id="filter_text" onkeydown="event.stopPropagation()" onkeyup="filter_function(event)" placeholder="Filter names.." style="width:100%;">'


s += '<table id="compatibility_table" style="width:100%">\n'
s += '<tr><th></th><th width="55%" onclick="w3.sortHTML(\'#compatibility_table\', \'.item\', \'td:nth-child(2)\')" style="cursor:pointer">Game title</th><th width="25%">Status</th></tr>'
for row in range(50):
  fuckup = ['x', 'a', 'm']
  game_title = fuckup[row % 3] + 'Foobar: Adventures of foo bar'

  if row == 0:
    game_title += "." * 56

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
  status_types = [
    ('Playable', 'green'), # Same as ingame, but only if no exit-reason is given
    ('Ingame', 'orange'), # Can go ingame
    ('Menu', 'black'), # Menu shows up
    ('Intro', 'black'), # Intro animations / logos play
    ('Nothing', 'gray') # Not even intro can be seen
  ]
  issue_types = [
    'Broken audio',
    'Broken graphics',
    'Slow'
  ]
  exit_reasons = [
    'Stuck', # Xbox waits / repeats same step or simply can't continue
    'Hangs', # PC is busy and never returns to emulation
    'Crashes', # Unexpected stop
    'Aborts' # Forced stop [assert etc.]
  ]
  covers = [
    ('Halo 2', 'https://www.mobygames.com/images/covers/l/38333-halo-2-xbox-front-cover.jpg'),
    ('Halo: Combat Evolved', 'https://vignette.wikia.nocookie.net/halo/images/8/81/Halo_Combat_Evolved_-_Xbox_Cover.png/revision/latest/scale-to-width-down/334?cb=20150331162657'),
    ('Burnout 2 (Developer\'s Cut)', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQq-EhuCr5Yzby_M-vJSbcmQMbINI1JKwceSdS5XLUPT8an8IKqKQ'),
    ('Tony Hawk\'s Underground 2', 'https://www.mobygames.com/images/covers/l/50495-tony-hawk-s-underground-2-xbox-front-cover.jpg'),
    ('Tony Hawk\'s Underground', 'https://www.mobygames.com/images/covers/l/26593-tony-hawk-s-underground-xbox-front-cover.jpg'),
    ('Tony Hawk\'s Pro Skater 4', 'https://www.mobygames.com/images/covers/l/15666-tony-hawk-s-pro-skater-4-xbox-front-cover.jpg'),
    ('Tony Hawk\'s Pro Skater 2X', 'https://www.mobygames.com/images/covers/l/12211-tony-hawk-s-pro-skater-2x-xbox-front-cover.jpg'),
    ('Midtown Madness 3', 'https://www.mobygames.com/images/covers/l/28406-midtown-madness-3-xbox-front-cover.jpg'),
    ('Mashed: Drive to Survive','http://xboxaddict.com/images/box_art/4298.jpg'),
    ('Mashed: Fully Loaded','https://images-na.ssl-images-amazon.com/images/I/512KWAXKC2L._SY445_.jpg'),
    ('Outrun 2','https://www.mobygames.com/images/covers/l/190011-outrun-2-xbox-front-cover.jpg'),
    ('Outrun 2006: Coast 2 Coast','https://www.mobygames.com/images/covers/l/118456-outrun-2006-coast-2-coast-xbox-front-cover.jpg'),
    ('Counter-Strike','https://images-na.ssl-images-amazon.com/images/I/517P1V6XNQL._AC_SX215_.jpg'),
    ('Mechassault','https://www.mobygames.com/images/covers/l/38621-mechassault-xbox-front-cover.jpg'),
    ('Fusion Frenzy','https://cdn4.spong.com/pack/f/u/fuzionfren54194/_-Fuzion-Frenzy-Xbox-_.jpg'), 
    ('Burnout 3: Takedown','https://www.mobygames.com/images/covers/l/194942-burnout-3-takedown-xbox-front-cover.png'),
    ('Shenmue 2','https://cdn3.spong.com/pack/s/h/shenmue291673/_-Shenmue-2-Xbox-_.jpg'),
    ('Star Wars: Battlefront','https://www.mobygames.com/images/covers/l/47712-star-wars-battlefront-xbox-front-cover.jpg'),
    ('Gunvalkyrie','https://www.mobygames.com/images/covers/l/216954-gunvalkyrie-xbox-front-cover.jpg'),
    ('Lego Star Wars II','https://www.mobygames.com/images/covers/l/190230-lego-star-wars-ii-the-original-trilogy-xbox-front-cover.png'),
    ('Crash Twinsanity','https://cdn1.spong.com/pack/c/r/crashtwins148671l/_-Crash-Twinsanity-Xbox-_.jpg'),
    ('Oddworld: Stranger\'s Wrath','https://www.mobygames.com/images/covers/l/128472-oddworld-stranger-s-wrath-xbox-front-cover.jpg')
  ]
  status_type, status_color = status_types[row % len(status_types)]
  issue_type = []
  for i in issue_types:
    issue_type += ['&#9888;&nbsp;%s' % i]
  for i in [exit_reasons[(row // 3) % len(exit_reasons)]]:
    issue_type += ['&#x1F5D9;&nbsp;%s' % i]
  #issue_type = [""] # ["&#x2714; No issues"]
  status = '<b style="color:%s">%s</b><br>%s' % (status_color, status_type, "<br>".join(issue_type))
  game_title,cover = covers[row % (len(covers))]
  s += '' + \
    '<tr class="item">' + \
      '<td>' + \
        '<img style="height: 128px; border:1px solid gray; text-align: center;" src="%s" />' % cover + \
      '</td><td>' + \
        '<b class="name">%s</b><br>' % (html.escape(game_title)) + \
        'Title-ID: %s' % (title_id) + \
      '</td><td>' + \
        '%s' % (status) + \
      '</td>' + \
    '</tr>\n'
s += '</table>\n'

with open('docs/compatibility.md', 'wb') as f:
  f.write(s.encode('utf-8'))
