#!/usr/bin/env python3
"""
FCO Training 2026 - JotForm Quiz Builder
Fills existing forms with questions, scoring, and email notifications.
"""

import requests
import json
import time

API_KEY = "4567ff4af1b777f8151f1fb062ff051b"
BASE = "https://api.jotform.com"

DIRECTOR_EMAILS = "lcfcoinc@gmail.com,fwfcoinc@gmail.com,pfcoinc@gmail.com"

# Existing form IDs (already created)
FORM_IDS = {
    1: "260605276355155",
    2: "260604637727158",
    3: "260604953148156",
    4: "260605230098149",
    5: "260605448390155",
    6: "260604761038151",
}

QUIZZES = [
    {
        "short": "Positive & Supportive Caregiver Child Interactions",
        "questions": [
            {"text": "When TRS evaluates your classroom, what are they primarily looking at?",
             "options": ["How well the children behave","How the teacher responds to children","How clean the classroom is","How many activities are planned"], "correct": 1},
            {"text": "When a one-year-old is upset, what is the best first step?",
             "options": ["Ignore it and wait for them to calm down","Name the emotion — 'It looks like you feel sad'","Send them to another classroom","Raise your voice to get their attention"], "correct": 1},
            {"text": "What is 'co-regulation'?",
             "options": ["Two teachers sharing a classroom","Helping a child calm their emotions by staying calm yourself","A meal count method","A TRS paperwork requirement"], "correct": 1},
            {"text": "When offering choices to a two-year-old, how many choices should you give?",
             "options": ["As many as they want","Five or more","Two simple choices","None — just tell them what to do"], "correct": 2},
            {"text": "For TRS scoring purposes, what do you NOT need to worry about?",
             "options": ["Staying calm and warm with children","Whether children have tantrums","Using positive descriptive language","Responding promptly to children's cues"], "correct": 1},
            {"text": "What should you say instead of 'Don't run!'?",
             "options": ["'Stop that immediately!'","'Walk, please' or 'Show me walking feet'","'I'll call your parents'","Nothing — just give them a look"], "correct": 1},
        ],
    },
    {
        "short": "Play-Based Learning: Let's Make Learning Fun",
        "questions": [
            {"text": "What is play-based learning?",
             "options": ["Giving children free time with no teacher involvement","Learning driven by child-initiated and teacher-guided play","Worksheets and structured lessons only","Screen time and tablet use"], "correct": 1},
            {"text": "How many times does a child need to do something through PLAY to learn it?",
             "options": ["400 times","100 times","50 times","20 times"], "correct": 3},
            {"text": "What is one easy, reusable sensory activity idea mentioned in the training?",
             "options": ["Bubble wrap popping","Laminated sheets inside a Ziploc bag with gel or pom-poms","iPad drawing apps","Coloring books"], "correct": 1},
            {"text": "What should you do when a child creates something during play-based learning?",
             "options": ["Just say 'Good job!'","Document it with a photo in ProCare and describe what they did","Keep it in the classroom forever","Ask them to do it again correctly"], "correct": 1},
            {"text": "What does the 'role of the teacher' mean in a play-based classroom?",
             "options": ["Sit back and let children do whatever they want","Observe, ask open-ended questions, and guide learning","Only do worksheets and avoid mess","Focus on test preparation"], "correct": 1},
            {"text": "Which of these is an example of an open-ended question during play?",
             "options": ["'Is that a castle?'","'Are you done?'","'What are you building and who lives inside it?'","'Stop playing and come to circle time'"], "correct": 2},
        ],
    },
    {
        "short": "Effective Communication with Parents",
        "questions": [
            {"text": "What is the 'sandwich method' for talking to parents?",
             "options": ["Start with a complaint, add praise, end with a complaint","Start positive, share your concern in the middle, end positive","Share all concerns first, then say something nice","Say whatever is on your mind"], "correct": 1},
            {"text": "When should you give parents your personal phone number?",
             "options": ["When they ask nicely","When it's an emergency","Never — always use ProCare or school channels","When you become close friends"], "correct": 2},
            {"text": "What pronouns should you use when talking with parents to build teamwork?",
             "options": ["'You' and 'your child'","'They' and 'them'","'We' and 'us'","'I' and 'me'"], "correct": 2},
            {"text": "What does TRS look for MORE than pictures in parent communication?",
             "options": ["Group posts with lots of emoji","Individual written notes and descriptions","Videos only","Monthly newsletters"], "correct": 1},
            {"text": "For difficult conversations with a parent, who should be involved?",
             "options": ["Only the teacher and the parent","The teacher, director, and a neutral third party","Only the director","The whole staff team"], "correct": 1},
            {"text": "Before sending a sensitive message through ProCare, what should you do?",
             "options": ["Send it quickly before you overthink it","Have your director or assistant director review it first","Post it on social media instead","Wait until next week"], "correct": 1},
        ],
    },
    {
        "short": "Food Program Training (CACFP)",
        "questions": [
            {"text": "What does CACFP stand for?",
             "options": ["Child and Adult Care Food Program","Childcare Audit Compliance and Food Protocol","Child Activity Curriculum and Food Plan","Care and Compliance Food Program"], "correct": 0},
            {"text": "If a child refuses to eat their green beans at lunch, what do you do?",
             "options": ["Remove them from the plate","Mark them absent for that meal","Keep all food components on the plate — they must be served even if not eaten","Give them an alternative food"], "correct": 2},
            {"text": "What type of milk must be served to children ages 2 and older?",
             "options": ["Whole milk","Two-percent milk","One-percent or fat-free skim milk","Any milk available in the store"], "correct": 2},
            {"text": "When should BLPs (meal counts) be completed?",
             "options": ["At the end of the day","At the end of the week","At the point of service — when the children are eating","Whenever is convenient"], "correct": 2},
            {"text": "How many food components are required at LUNCH?",
             "options": ["2","3","4","5"], "correct": 3},
            {"text": "What ink color must teachers use on roll sheets and BLPs?",
             "options": ["Red ink only","Any color is fine","Black ink only","Blue ink preferred"], "correct": 2},
        ],
    },
    {
        "short": "Supporting Children of All Abilities",
        "questions": [
            {"text": "What organization is the national standard for speech and language development milestones?",
             "options": ["CDC","ASHA (American Speech and Hearing Association)","TRS (Texas Rising Star)","AAP (American Academy of Pediatrics)"], "correct": 1},
            {"text": "What therapy helps children with handwriting, low muscle tone, and sensory issues?",
             "options": ["Physical therapy (PT)","Speech therapy (ST)","Occupational therapy (OT)","Behavioral therapy"], "correct": 2},
            {"text": "Which insurance does River Kids Therapy currently have a temporary pause with?",
             "options": ["Medicaid","TRICARE","Blue Cross Blue Shield","Aetna"], "correct": 2},
            {"text": "What has been dramatically increasing since 2007, according to the training?",
             "options": ["Food allergies","Autism diagnoses","Speech delays due to screens","Physical therapy referrals"], "correct": 1},
            {"text": "Where does River Kids Therapy provide services?",
             "options": ["Only in their clinic","Only at hospitals","At homes or daycare/school locations","Only on weekends"], "correct": 2},
            {"text": "What should you do if you notice a child may need speech or therapy services?",
             "options": ["Wait and see for a year","Diagnose the child yourself","Refer the family to River Kids using the QR code card or your director","Keep it private"], "correct": 2},
        ],
    },
    {
        "short": "Tech Training: ChildcareEd Continuing Education",
        "questions": [
            {"text": "What email address should you use to log into ChildcareEd?",
             "options": ["Your personal Gmail","Your school's general email","The email address linked to your Paychex account","Any email you prefer"], "correct": 2},
            {"text": "If it's your first time logging into ChildcareEd, what do you do?",
             "options": ["Create a brand new account","Call Crystal to set it up","Click 'Forgot Password' to set your password","Use the username 'FCOstaff'"], "correct": 2},
            {"text": "How do you request a specific online course from ChildcareEd?",
             "options": ["Just enroll yourself and start it","Copy the course URL and email it to Crystal and your director","Ask a coworker to sign you up","Print it out and bring it to the office"], "correct": 1},
            {"text": "How many total training hours does TRS require per year?",
             "options": ["10 hours","20 hours","24 hours","30 hours"], "correct": 3},
            {"text": "What is available through ChildcareEd for staff who want to advance their career?",
             "options": ["A college degree","CDA (Child Development Associate) certification","A director's license","A Texas teacher certification"], "correct": 1},
            {"text": "What is one nice thing about ChildcareEd compared to Tim the Trainer?",
             "options": ["It's always free with no credits needed","There's a much wider variety of courses you can choose based on your interests and age group","You only have to do it once ever","It counts for more hours automatically"], "correct": 1},
        ],
    },
]


def add_question(form_id, q_data):
    url = f"{BASE}/form/{form_id}/questions"
    r = requests.post(url, params={"apiKey": API_KEY}, data=q_data)
    try:
        resp = r.json()
        qid = resp.get("content", {}).get("qid")
        return qid
    except Exception:
        print(f"    ERROR: {r.status_code} {r.text[:200]}")
        return None


def add_email(form_id, email_data):
    url = f"{BASE}/form/{form_id}/emails"
    r = requests.post(url, params={"apiKey": API_KEY}, data=email_data)
    try:
        return r.json()
    except Exception:
        print(f"    EMAIL ERROR: {r.status_code} {r.text[:200]}")
        return {}


def fill_quiz(quiz_num, form_id, quiz_data):
    short = quiz_data["short"]
    print(f"\n{'='*60}")
    print(f"Filling Quiz {quiz_num}: {short}")
    print(f"Form ID: {form_id}")
    print("="*60)

    order = 1

    # Header
    qid = add_question(form_id, {
        "question[type]": "control_head",
        "question[text]": "🏫 FCO Staff Training 2026",
        "question[subHeader]": f"Quiz {quiz_num} of 6 · {short}",
        "question[order]": order,
    })
    print(f"  ✅ Header (qid={qid})")
    order += 1
    time.sleep(0.3)

    # Staff full name
    qid = add_question(form_id, {
        "question[type]": "control_fullname",
        "question[text]": "Your Full Name",
        "question[required]": "Yes",
        "question[order]": order,
        "question[name]": "staffName",
        "question[middle]": "No",
        "question[prefix]": "No",
        "question[suffix]": "No",
    })
    print(f"  ✅ Name field (qid={qid})")
    order += 1
    time.sleep(0.3)

    # Staff email
    qid = add_question(form_id, {
        "question[type]": "control_email",
        "question[text]": "Your Email Address",
        "question[required]": "Yes",
        "question[order]": order,
        "question[name]": "staffEmail",
    })
    print(f"  ✅ Email field (qid={qid})")
    order += 1
    time.sleep(0.3)

    # School location dropdown
    qid = add_question(form_id, {
        "question[type]": "control_dropdown",
        "question[text]": "Your School Location",
        "question[required]": "Yes",
        "question[order]": order,
        "question[name]": "schoolLocation",
        "question[options]": "League City|Friendswood|Pearland",
    })
    print(f"  ✅ School location dropdown (qid={qid})")
    order += 1
    time.sleep(0.3)

    # Quiz questions with calcValues scoring
    q_names = []
    for i, q in enumerate(quiz_data["questions"]):
        qname = f"question{i+1}"
        q_names.append(qname)
        # Build calcValues: 1 for correct, 0 for wrong
        calc_vals = "|".join("1" if j == q["correct"] else "0" for j in range(len(q["options"])))
        qid = add_question(form_id, {
            "question[type]": "control_radio",
            "question[text]": f"{i+1}. {q['text']}",
            "question[required]": "Yes",
            "question[order]": order,
            "question[name]": qname,
            "question[options]": "|".join(q["options"]),
            "question[calcValues]": calc_vals,
            "question[allowOther]": "No",
        })
        print(f"  ✅ Q{i+1} (qid={qid}, correct={q['options'][q['correct']][:30]})")
        order += 1
        time.sleep(0.4)

    # Score calculation (hidden, sums all calcValues)
    formula = " + ".join([f"{{{n}_calcValue}}" for n in q_names])
    qid = add_question(form_id, {
        "question[type]": "control_calculation",
        "question[text]": "Your Score",
        "question[formula]": formula,
        "question[order]": order,
        "question[name]": "totalScore",
        "question[hidden]": "Yes",
        "question[suffix]": " / 6",
        "question[defaultValue]": "0",
    })
    print(f"  ✅ Score calculation field (qid={qid})")
    order += 1
    time.sleep(0.4)

    # Director notification email
    notif = add_email(form_id, {
        "type": "notification",
        "from": "noreply@jotform.com",
        "fromname": "FCO Training Portal",
        "to": DIRECTOR_EMAILS,
        "subject": f"[FCO Training] Quiz {quiz_num} Submission – {{staffName}} ({{schoolLocation}}) – Score: {{totalScore}}/6",
        "html": "Yes",
        "body": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
<div style="background:#1d4ed8;color:white;padding:24px;border-radius:8px 8px 0 0;text-align:center">
  <h2 style="margin:0">🏫 FCO Staff Training 2026</h2>
  <p style="margin:6px 0 0;opacity:.85">Quiz {quiz_num} of 6: {short}</p>
</div>
<div style="background:white;padding:28px;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 8px 8px">
  <table style="width:100%;border-collapse:collapse">
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b;width:140px">Staff Member</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-weight:600">{{staffName}}</td></tr>
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b">Email</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9">{{staffEmail}}</td></tr>
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b">School</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9">{{schoolLocation}}</td></tr>
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b">Score</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-weight:700;color:#16a34a">{{totalScore}} / 6</td></tr>
    <tr><td style="padding:8px 0;color:#64748b">Submitted</td><td style="padding:8px 0">{{submissionDate}}</td></tr>
  </table>
  <p style="color:#64748b;font-size:.82rem;margin-top:20px">FCO Training Portal · forchildrenonlydayschool.com</p>
</div>
</div>""",
    })
    print(f"  ✅ Director notification → {DIRECTOR_EMAILS}")
    time.sleep(0.4)

    # Staff certificate autoresponder
    cert = add_email(form_id, {
        "type": "autoresponder",
        "from": "noreply@jotform.com",
        "fromname": "For Children Only Day School",
        "to": "{staffEmail}",
        "subject": f"🎓 Your Certificate – FCO Training Quiz {quiz_num}: {short}",
        "html": "Yes",
        "body": f"""<div style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto">
<div style="background:linear-gradient(135deg,#1d4ed8,#2563eb);color:white;padding:32px;border-radius:8px 8px 0 0;text-align:center">
  <div style="font-size:52px;margin-bottom:8px">🎓</div>
  <h1 style="margin:0 0 4px;font-size:1.7rem;letter-spacing:-0.5px">Certificate of Completion</h1>
  <p style="margin:0;opacity:.85;font-size:.95rem">For Children Only Day School · 2026 Training Day</p>
</div>
<div style="background:white;padding:40px 36px;border:3px solid #1d4ed8;border-top:none;border-radius:0 0 8px 8px;text-align:center">
  <p style="color:#64748b;margin:0 0 10px;font-size:.95rem">This certifies that</p>
  <div style="font-size:2rem;font-weight:700;color:#1e293b;font-style:italic;border-bottom:2px solid #e2e8f0;padding-bottom:18px;margin-bottom:18px">{{staffName}}</div>
  <p style="color:#1e293b;font-size:1rem;margin:0 0 6px">has successfully completed</p>
  <p style="color:#1d4ed8;font-weight:700;font-size:1.15rem;margin:0 0 24px">Quiz {quiz_num} of 6: {short}</p>
  <div style="background:#f0fdf4;border:2px solid #16a34a;border-radius:10px;padding:14px 24px;display:inline-block;margin-bottom:24px">
    <span style="color:#16a34a;font-weight:700;font-size:1.2rem">Score: {{totalScore}} / 6 ✅</span>
  </div>
  <div style="color:#64748b;font-size:.9rem;margin-bottom:6px"><strong>School:</strong> {{schoolLocation}}</div>
  <div style="color:#64748b;font-size:.9rem;margin-bottom:28px"><strong>Date Completed:</strong> {{submissionDate}}</div>
  <hr style="border:none;border-top:2px solid #e2e8f0;margin:0 0 20px"/>
  <p style="color:#1d4ed8;font-weight:700;font-size:1rem;margin:0">For Children Only Day School</p>
  <p style="color:#94a3b8;font-size:.8rem;margin:4px 0 0">forchildrenonlydayschool.com · Friendswood · League City · Pearland</p>
</div>
<p style="text-align:center;color:#94a3b8;font-size:.78rem;margin-top:16px">You can print or save this email as your certificate of completion.</p>
</div>""",
    })
    print(f"  ✅ Certificate autoresponder → staff email")
    time.sleep(0.4)

    form_url = f"https://form.jotform.com/{form_id}"
    print(f"  🌐 {form_url}")
    return form_url


def main():
    results = []
    for quiz_num, quiz_data in enumerate(QUIZZES, 1):
        form_id = FORM_IDS[quiz_num]
        url = fill_quiz(quiz_num, form_id, quiz_data)
        results.append({
            "quiz_num": quiz_num,
            "form_id": form_id,
            "form_url": url,
            "title": quiz_data["short"],
        })
        time.sleep(1)

    print(f"\n{'='*60}")
    print("ALL DONE — SUMMARY")
    print("="*60)
    for r in results:
        print(f"Quiz {r['quiz_num']}: https://form.jotform.com/{r['form_id']}")

    with open("jotform-results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n✅ Saved to jotform-results.json")


if __name__ == "__main__":
    main()
