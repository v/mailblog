import re

sample_list = [
    'On Sat, Nov 10, 2012 at 12:18 PM, Kike Ibe <kikeibe@gmail.com> wrote:',
    'On Fri, Nov 9, 2012 at 3:07 AM, Nicole Shih <nicole.shih.1993@gmail.com>wrote:',
    'On Fri, Nov 9, 2012 at 3:07 AM, Nicole Shih <nicole.shih.1993@gmail.com>w=r=o=t=e:',
    'On Oct 10, 2012 at 9:20 AM, Shridatt Sugrim\n<ssugrim@winlab.rutgers.edu> wrote:',
    'On Oct 10, 2012, at 1:05 PM, Vaibhav Verma <vaibhav2614@gmail.com> wrote:\n      ',
    'On Wed, Oct 10, 2012 at 9:44 AM, Bilal Quadri (Google Drive) <\nbilalquadri92@gmail.com> wrote:',
    'On Oct 31, 2012 2:41 AM, "Vaibhav Verma" <vaibhav2614@gmail.com> wrote:',
# seriously sample8 is really fucked up!!,
    'On Thursday, October 4, 2012, Yesika Reyes wrote:',
    'On Thursday, October 4, 2012 3:03:14 AM UTC-4, Devon Peticolas wrote:',
    'On Fri, Aug 10, 2012 at 3:46 PM, Devon Peticolas <devon.peticolas@gmail.com=\n>',
    'On 10 November 2012 13:54, Vaibhav Verma <vaibhav2614@gmail.com> wrote:',
    'On Mon, May 21, 2012 at 9:12 AM, Vaibhav Verma <vaibhav2614@gmail.com> wrot=\ne:\n',
    'On Sun, May 6, 2012 at 7:16 AM, Vaibhav Verma <vaibhav2614@gmail.com> wrote:\n',
    '-----Original Message-----\n',
    '------- 1 of 1  -------\n'
]

def unquote(email):

    email_pattern = '<.*@.*\.(edu|com)(=)?\s*>'
    name_pattern = '(")?\w+\s*\w+(")?\s*(\(Google\s+Drive\))?'
    day_pattern = '(Sun(day)?|Mon(day)?|Tue(sday)?|Wed(nesday)?|Thu(rsday)?|Fri(day)?|Sat(urday)?)'
    month_pattern ='(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)'
    year_pattern = '\d{4}(,)?'
    time_pattern = '\d{1,2}:\d{2}(:\d{2})?\s*(PM|AM)?\s*(UTC-4)?'
    wrote_pattern = 'w\s*(=)?\s*r(=)?\s*o(=)?\s*t(=)?\s*e(=)?\s*:'
    date_pattern = '([0-3])?[0-9](,)?'
   
    original_dash_pattern = '(\-)+\s*Original\s*Message\s*(\-)+\s*'
    numbered_dash_pattern = '(\-)+\s*\d+\s*of\s*\d+\s*(\-)+\s*'

    google_style_reply =  'On\s*({day_pattern},)?\s*({date_pattern})?\s*{month_pattern}\s*\
({date_pattern})?\s*{year_pattern}\s*(at)?\s*({time_pattern},)?\s*{name_pattern}\s*({email_pattern})?\s*({wrote_pattern})?\s*'.format(
        day_pattern = day_pattern,
        email_pattern = email_pattern,
        name_pattern = name_pattern,
        month_pattern = month_pattern,
        year_pattern = year_pattern,
        time_pattern = time_pattern,
        wrote_pattern = wrote_pattern,
        date_pattern = date_pattern
        )

    patterns = [ google_style_reply,original_dash_pattern,numbered_dash_pattern ]
    god_regex_str = '({0})'.format('|'.join(patterns))
    quoted_reply_regex =  re.compile(god_regex_str,re.IGNORECASE | re.DOTALL)
    m = quoted_reply_regex.search(email)
    if m:
        return email[:m.start()]
    return email
