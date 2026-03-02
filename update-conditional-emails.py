#!/usr/bin/env python3
"""
FCO Training 2026 - Update JotForm conditional director notifications
Each quiz notifies ONLY the director of the school the staff member selected.
School location is qid=4 on all forms.
"""

import requests
import json
import time

API_KEY = "4567ff4af1b777f8151f1fb062ff051b"
BASE = "https://api.jotform.com"

FORM_IDS = {
    1: "260605276355155",
    2: "260604637727158",
    3: "260604953148156",
    4: "260605230098149",
    5: "260605448390155",
    6: "260604761038151",
}

QUIZ_TITLES = {
    1: "Positive & Supportive Caregiver Child Interactions",
    2: "Play-Based Learning: Let's Make Learning Fun",
    3: "Effective Communication with Parents",
    4: "Food Program Training (CACFP)",
    5: "Supporting Children of All Abilities",
    6: "Tech Training: ChildcareEd Continuing Education",
}

DIRECTORS = {
    "League City":  "lcfcoinc@gmail.com",
    "Friendswood":  "fwfcoinc@gmail.com",
    "Pearland":     "pfcoinc@gmail.com",
}


def build_notification_body(quiz_num, school, director_email, short_title):
    """Build a clean HTML notification email body."""
    return f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">
<div style="background:#1d4ed8;color:white;padding:24px;border-radius:8px 8px 0 0;text-align:center">
  <h2 style="margin:0">🏫 FCO Staff Training 2026</h2>
  <p style="margin:6px 0 0;opacity:.85">Quiz {quiz_num}: {short_title}</p>
</div>
<div style="background:white;padding:28px;border:1px solid #e2e8f0;border-top:none;border-radius:0 0 8px 8px">
  <p style="margin:0 0 16px;color:#64748b;font-size:.9rem">A staff member at <strong style="color:#1d4ed8">{school}</strong> completed a training quiz:</p>
  <table style="width:100%;border-collapse:collapse;font-size:.95rem">
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b;width:150px">Staff Member</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-weight:600">{{staffName}}</td></tr>
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b">Email</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9">{{staffEmail}}</td></tr>
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b">School</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9">{{schoolLocation}}</td></tr>
    <tr><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;color:#64748b">Score</td><td style="padding:8px 0;border-bottom:1px solid #f1f5f9;font-weight:700;color:#16a34a">{{totalScore}} / 6</td></tr>
    <tr><td style="padding:8px 0;color:#64748b">Submitted</td><td style="padding:8px 0">{{submissionDate}}</td></tr>
  </table>
  <p style="color:#64748b;font-size:.82rem;margin-top:20px;border-top:1px solid #f1f5f9;padding-top:16px">
    FCO Training Portal · forchildrenonlydayschool.com
  </p>
</div>
</div>"""


def build_certificate_body(quiz_num, short_title):
    """Build the staff certificate autoresponder email."""
    return f"""<div style="font-family:Arial,sans-serif;max-width:640px;margin:0 auto">
<div style="background:linear-gradient(135deg,#1d4ed8,#2563eb);color:white;padding:32px;border-radius:8px 8px 0 0;text-align:center">
  <div style="font-size:52px;margin-bottom:8px">🎓</div>
  <h1 style="margin:0 0 4px;font-size:1.7rem">Certificate of Completion</h1>
  <p style="margin:0;opacity:.85;font-size:.95rem">For Children Only Day School · 2026 Training Day</p>
</div>
<div style="background:white;padding:40px 36px;border:3px solid #1d4ed8;border-top:none;border-radius:0 0 8px 8px;text-align:center">
  <p style="color:#64748b;margin:0 0 10px;font-size:.95rem">This certifies that</p>
  <div style="font-size:2rem;font-weight:700;color:#1e293b;font-style:italic;border-bottom:2px solid #e2e8f0;padding-bottom:18px;margin-bottom:18px">{{staffName}}</div>
  <p style="color:#1e293b;font-size:1rem;margin:0 0 6px">has successfully completed</p>
  <p style="color:#1d4ed8;font-weight:700;font-size:1.15rem;margin:0 0 24px">Quiz {quiz_num} of 6: {short_title}</p>
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
</div>"""


def update_form(quiz_num, form_id):
    short = QUIZ_TITLES[quiz_num]
    print(f"\n{'='*60}")
    print(f"Quiz {quiz_num}: {short}")
    print(f"Form: {form_id}")
    print("="*60)

    # Step 1: get current emails to preserve the autoresponder
    r = requests.get(f"{BASE}/form/{form_id}/properties",
                     params={"apiKey": API_KEY})
    existing = r.json().get("content", {}).get("emails", [])

    # Keep autoresponder, rebuild everything else
    autoresponder = None
    for e in existing:
        if e.get("type") == "autorespond":
            autoresponder = e
            break

    # Step 2: build 3 conditional notification emails (one per school)
    new_emails = []
    conditions = []
    cond_id = 1

    for school, director_email in DIRECTORS.items():
        uid = f"{form_id}{cond_id}notif"
        email_obj = {
            "type": "notification",
            "name": f"Director – {school}",
            "from": "{staffName}",
            "fromname": "FCO Training Portal",
            "replyTo": "{staffEmail}",
            "to": director_email,
            "subject": f"[FCO Training] Quiz {quiz_num} – {{staffName}} ({school}) – Score: {{totalScore}}/6",
            "html": "1",
            "body": build_notification_body(quiz_num, school, director_email, short),
            "sendOnSubmit": "1",
            "sendOnEdit": "0",
            "uniqueID": uid,
            "hideEmptyFields": "1",
        }
        new_emails.append(email_obj)

        # Condition: send this email only if schoolLocation equals this school
        # field "4" = qid of schoolLocation dropdown
        conditions.append({
            "id": str(cond_id),
            "link": "Any",
            "terms": [
                {
                    "field": "4",
                    "operator": "eq",
                    "value": school
                }
            ],
            "action": [
                {
                    "action": "sendEmail",
                    "email": uid
                }
            ]
        })
        cond_id += 1

    # Step 3: rebuild the staff certificate autoresponder
    cert_uid = f"{form_id}cert"
    cert_email = {
        "type": "autorespond",
        "name": "Staff Certificate",
        "from": "Taylor Powell",
        "fromname": "For Children Only Day School",
        "replyTo": "TaylorPowell@ForChildrenOnlyBiz.onmicrosoft.com",
        "to": "{staffEmail}",
        "subject": f"🎓 Your Certificate – FCO Training Quiz {quiz_num}: {short}",
        "html": "1",
        "body": build_certificate_body(quiz_num, short),
        "sendOnSubmit": "1",
        "sendOnEdit": "0",
        "uniqueID": cert_uid,
        "hideEmptyFields": "1",
    }
    new_emails.append(cert_email)

    # Step 4: PUT updated emails + conditions to form properties (JSON body required)
    payload = {
        "properties": {
            "emails": new_emails,
            "conditions": conditions,
        }
    }
    resp = requests.put(
        f"{BASE}/form/{form_id}/properties",
        params={"apiKey": API_KEY},
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    result = resp.json()
    rc = result.get("responseCode")
    msg = result.get("message", "")
    print(f"  PUT properties → {rc} {msg}")

    if rc == 200:
        print(f"  ✅ 3 conditional director notifications set")
        print(f"     → League City:  lcfcoinc@gmail.com  (if school = League City)")
        print(f"     → Friendswood:  fwfcoinc@gmail.com  (if school = Friendswood)")
        print(f"     → Pearland:     pfcoinc@gmail.com   (if school = Pearland)")
        print(f"  ✅ Staff certificate autoresponder preserved")
    else:
        print(f"  ❌ Error: {json.dumps(result)[:300]}")

    time.sleep(1)
    return rc == 200


def main():
    success = 0
    for quiz_num, form_id in FORM_IDS.items():
        ok = update_form(quiz_num, form_id)
        if ok:
            success += 1

    print(f"\n{'='*60}")
    print(f"Done: {success}/6 forms updated successfully")
    print("="*60)


if __name__ == "__main__":
    main()
