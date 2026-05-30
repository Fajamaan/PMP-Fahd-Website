# -*- coding: utf-8 -*-
# Builds a single self-contained index.html quiz app from questions_data.js + answer key.
import os

BUILD = r'C:\Users\Fajam\MyClaude\build'
OUT = r'C:\Users\Fajam\MyClaude\PMP-Quiz'
REPO_ROOT = r'C:\Users\Fajam\MyClaude'  # also emit a root index.html for web hosting (Hostinger, etc.)
SITE_DEPLOY = r'C:\Users\Fajam\pmp-fahd-site'  # clean static-only repo Hostinger deploys from

# Answer key, in order Q1..Q228 (matches questions_dump.txt numbering).
# Each entry: (correct_letters, short_explanation)
# correct_letters: e.g. "A" or "A,B,D" for multi-select (Select two/three).
ANSWERS = [
("A","Withdraw/avoid (avoidance) only postpones the conflict; the parties retreat, so it is never a permanent resolution."),
("D","Open dialogue where everyone shares viewpoints and consensus is reached is Collaborate/problem-solve, the win-win technique."),
("B","Conflict is a natural, inevitable part of any project environment - a reassuring fact for a new PM."),
("A","Collaborate/problem-solve is the win-win technique PMs should use most often."),
("B","Reaching consensus after open discussion (incorporating the sponsor's view) is Collaborate/problem-solve."),
("A","The top sources of conflict are competing/conflicting interests, scarce resources, schedules and priorities."),
("B","Personality clashes are NOT among the top sources; the real top three are work styles, scheduling priorities, and scarce resources."),
("C","Each side gives up something (limited test now, full test later) - that is a Compromise."),
("C","Team members are first responsible for resolving their own conflicts; the PM steps in only if they cannot."),
("A,B,D","Servant leaders promote self-awareness, coach rather than control, and help others grow. Strong conviction is a charismatic trait."),
("D","Leading through inspiration, high energy and strong conviction describes a Charismatic leader."),
("D","A servant leader facilitates the team's discovery and definition of the work rather than directing it."),
("A,B,D","Servant-leader behaviors include listening, coaching and promoting self-awareness - not controlling."),
("A,B,C","Leaders use referent power, impart vision, and focus on strategic plans. Satisfying day-to-day stakeholder needs is management."),
("D","Being unable to reach any decision points to a missing decision-making criterion in the team charter."),
("D","Having each member state their name and country surfaces and values the team's diversity at kickoff."),
("B","Discomfort and disorientation in an unfamiliar culture, despite prep, is culture shock."),
("D","Fairness does not 'encompass diversity training and preventing culture shock' - that statement is false."),
("E","All statements about diversity and inclusion are true."),
("A,C,D","Individual performance appraisals draw on work performance reports, the resource management plan, and team performance assessments."),
("A","Observation and conversation is the technique used to gauge team members' attitudes."),
("C","360-degree feedback is a form of project (individual) performance appraisal."),
("A","Team performance assessments determine and document a team's effectiveness."),
("C","Feedback on what went well/poorly and benefits achieved is captured in the lessons learned register."),
("B,C,D","Structured interviews, ability tests and attitudinal surveys reveal team strengths/weaknesses; training is not an assessment tool."),
("A,D","Servant leadership empowers teams through greater accountability and through mentoring/encouragement."),
("B","Provide training for Hal (and anyone else who needs it) on the new program."),
("C","Direct a colleague struggling with project complexity to the PMO for support and standards."),
("D","Training needs and plans for the team are documented in the resource management plan."),
("A","Knowledge that can be codified with words, numbers and images is explicit knowledge."),
("C","Manage Project Knowledge runs throughout the project, not only at the end of Executing - that statement is false."),
("D","Tacit knowledge is hard to express - beliefs, experiences and know-how."),
("A,B,D","Daily stand-up questions: what did I complete, what will I do next, and what are my impediments."),
("D","Facilitating consensus, influencing stakeholders and negotiating agreements requires interpersonal (and team) skills."),
("B,C,D","When building a team the PM negotiates with functional managers, other project managers, and vendors/external organizations."),
("D","Facilitate team-building activities to rebuild a collaborative, cooperative environment after major turnover."),
("A","Negotiate with the director to keep the resource."),
("B","The criteria confirming a story is complete and ready for use is the Definition of Done."),
("B","An impasse over contested contract terms is resolved through Alternative Dispute Resolution (ADR)."),
("D","A project is complete only when the customer gives formal documented acceptance."),
("D","Reviewing what went well/poorly with the vendor is capturing lessons learned."),
("B","Acceptance criteria are found in the requirements documentation."),
("B","Preparing/sizing stories for the upcoming iteration is backlog refining (grooming)."),
("C","A war room brings the team together physically (co-location) to collaborate intensely."),
("C","Add training and mentorship for the new team member rather than removing or reassigning."),
("A,B,D","Successful Agile teams rest on foundational trust, an Agile mindset, and a safe working environment."),
("D","Team-building activities build trust among the team."),
("C","Give your friend a chance to report accurate status; if not, report the slippage accurately yourself."),
("D","A manager who listens, adjusts, and trusts you to fix it practices Theory Y."),
("A","Cooperate fully with a PMI Code of Ethics investigation."),
("A,C","Remote pairing via video and an ongoing 'fishbowl' video feed create virtual workspaces."),
("D","Being 'closer to customers and suppliers' is not a listed benefit of virtual teams."),
("D","Negotiation is used to secure a key resource already committed elsewhere."),
("D","An all-day open video feed simulating a shared open workspace is a fishbowl window."),
("D","Availability, capabilities and skills of current/future resources are captured in the resource calendar/pool."),
("B,C,D","True: members must understand expectations and decision-making, communication protocols, and get credit. Different locations do NOT mean different goals."),
("E","A team charter captures ground rules, working agreements and group norms."),
("B","The meeting broke down because the PM had not set clear ground rules."),
("D","Osmotic communication is a polite form of eavesdropping in an open workspace."),
("A","It is beneficial - but not strictly necessary - for ALL team members to have EI; saying it is necessary for all is the false statement."),
("C","Cross-cultural communication risks the meaning of the message not being understood."),
("A,C,D","Interpersonal/team skills to manage a team: conflict management, emotional intelligence, and influencing."),
("D","Listening, supporting and trusting the team reflects Theory Y."),
("A","Expectancy Theory: the expectation of a positive outcome drives motivation."),
("A","The resources are operating at different levels of Maslow's Hierarchy of Needs."),
("B","Project manager is not a defined Agile role; the others (cross-functional member, product owner, team facilitator) are."),
("D","A key benefit of rapid (incremental) delivery is the ability to get feedback early and often."),
("C,D","Lateral thinking was coined by Edward de Bono and is reasoning about problems from non-obvious perspectives."),
("C","De Bono's lateral thinking can be used as alternatives analysis to determine scope."),
("A","You + 4 stakeholders = 5 people, so n(n-1)/2 = 10 communication channels."),
("C","12 people = 66 channels; 66 - 45 = 21 additional channels."),
("D","Timeboxing with successive prototypes to reduce uncertainty describes an iterative life cycle."),
("C","Staying calm and handling the outburst privately upholds the value of Respect."),
("A","Changes approved because of the submitter's position use legitimate (positional) power."),
("D","A team that is not yet open and trusting and is clashing is in the Storming stage."),
("A,B,C","Influencing means getting things done, understanding formal/informal structures, and using power and politics."),
("B","Antwon, the director who was formally named sponsor, is the correct project sponsor."),
("B,C,D","Reward/recognition should be proportional to achievement and linked to performance, and can backfire if misused."),
("D","At minimum, stakeholder satisfaction is measured during project closure."),
("A","The stakeholder engagement assessment matrix lets you quickly evaluate current vs desired engagement."),
("D","The PM failed to transition ongoing support/maintenance to the operational team."),
("A","Smoothing (accommodating) emphasizes areas of agreement over areas of difference."),
("C","A normal, successful completion with a celebration is project ending by extinction."),
("C","Lying on an application to obtain a role is an ethics violation."),
("A","Classifying stakeholders (resistant/unaware/neutral/supportive/leading) uses data representation (engagement matrix)."),
("D","Resource smoothing keeps the project on schedule by adjusting within available float (no critical-path change)."),
("C","Agile feedback is used to improve the product, not merely 'plan the next part' - that statement is the exception."),
("B","Knowledge, skills and behaviors to guide, motivate and direct a team are leadership skills."),
("B,D","Agile teams favor value-based and empirical (observed) performance measurements."),
("A,B,D","A social contract addresses team values, ground rules and group norms - not task assignments."),
("C","The product owner represents stakeholders and is the liaison among stakeholders, Scrum master and dev team."),
("A","Inability to connect the project to organizational goals signals a gap in business management/strategic skills."),
("D","Taking a role he was not qualified for violated Responsibility (accept only assignments you are qualified for)."),
("B","The salience model classifies stakeholders by power, urgency and legitimacy."),
("C","Remaining work effort for a sprint is shown on a burndown chart."),
("C","Training on cultural norms to build relationships is part of Manage Stakeholder Engagement."),
("A","Two members lobbying the PM and unable to agree reflects the Storming stage."),
("A,D","Agile teams are typically 3-9 members and 100% dedicated."),
("B","The Conscientiousness spectrum runs from efficient to careless."),
("D","Measuring schedule performance against the baseline is a Monitoring and Controlling activity."),
("B","In a predictive life cycle the WBS is the basis for estimating costs."),
("A","Prototypes provide early feedback on the requirements."),
("B","A to-do/doing/done board focused on finishing work and limiting WIP is Kanban."),
("B","Determine Budget also outputs project funding requirements (with the cost baseline)."),
("A,B,D","OBS, BOM and RBS are hierarchical like a WBS; a RAM is a matrix."),
("B","In a predictive project, fast-tracking is the preferred (no added cost) way to finish a week earlier."),
("A,B,D","An Agile PMO is value-driven, invitation-oriented and multidisciplinary."),
("B","A PMO that consults and supports (templates, best practices) with low control is a Supportive PMO."),
("A","Perform Integrated Change Control is part of Monitoring and Controlling, not Executing - that statement is the exception."),
("B","Documenting how the project is executed, monitored and closed defines the project management plan."),
("A,B,D","Control charts: measure in/out of control, use the rule of seven, and plot common-cause variation."),
("C","Availability, cost and ability are team-member selection criteria."),
("D","Constraints identified early are recorded and updated in the assumption log."),
("E","Continuous integration, test at all levels, TDD and spikes are all technical practices that speed delivery."),
("B","Capturing lessons learned and archiving them in the final report is administrative (project) closure."),
("A","All project life cycles share a degree of uncertainty (greatest at the start)."),
("C","Deciding how budget performance will be measured is developing the cost management plan."),
("B","Appraisal costs are spent examining the product/process to verify requirements are met."),
("B","Communication requirements, escalation paths and the meeting list are in the communications management plan."),
("A","Philip Crosby promoted 'do it right the first time' (zero defects)."),
("A","Five low-priority risks are documented on a watch list."),
("C","Reliable data plus high accuracy with little effort points to parametric estimating."),
("C","Overall project risk is the effect of uncertainty on the project as a whole."),
("D","EAC = AC + (BAC - EV) = 425 + (900 - 475) = 850."),
("B","Guidance on releasing resources is in the project management plan (resource management plan)."),
("B","Losing critical resources mid-project causing it to wither is ending by Starvation."),
("B","Checking whether enough contingency/management reserve remains is reserve analysis."),
("B","Planned value is the value of work planned to be completed."),
("C","A good status review meeting uses an interactive communication method."),
("B","Perform data analysis to determine the corrective action needed to get back on plan."),
("B","Heavy up-front planning with minimal change afterward is a predictive life cycle."),
("B","Delivering highest-business-value items first is characteristic of an adaptive (Agile) life cycle."),
("B","Reviewing progress and lessons learned after a sprint is the sprint retrospective."),
("D","Buying insurance to offload a liability is a Transfer risk response."),
("B","Three-point estimating improves estimates by accounting for risk and uncertainty."),
("D","Acting on delayed critical activities with the sponsor is corrective action."),
("B","The lessons learned register records challenges, problems, realized risks and opportunities."),
("D","A milestone has zero duration; '30 Days' shows the PM misunderstands what a milestone is."),
("A","If a response is not fully effective, implement the fallback plan."),
("D","The team collectively focusing on one issue until resolved is swarming."),
("D","Prioritized list of user stories/features for upcoming releases is the product backlog."),
("B","Allowable budget-overage thresholds are defined in the cost management plan."),
("C","To vote on accepting a deliverable, the committee references the verified deliverables (from Control Quality)."),
("B","Many initiatives managed together toward one strategic goal is a program."),
("B","Coordinating paperwork for a change with no authority describes a project expediter."),
("D","A feasibility study can be the project's first phase or a standalone project."),
("A","Lessons learned can and should be documented throughout the project, not only at closing."),
("A","An internal organizational policy/procedure is an organizational process asset."),
("C","Gathering, integrating and disseminating outputs of all processes is the role of the PMIS."),
("C","Change management can be planned via management plans or a dedicated change management plan."),
("C","First assess the impact on scope and cost, then write the change request."),
("C","When a project is cancelled, follow the project closure procedures."),
("B","Sunk costs (already spent) are excluded from the project budget."),
("C","A control account manages scope/cost/schedule at a level above the work package."),
("B","Validate Scope usually follows Control Quality, secures customer acceptance, and surfaces differences of opinion."),
("C","The scope management plan does not cover how to determine deliverable correctness (that is quality/Control Quality)."),
("C","The WBS dictionary defines the work-package scope, helping control gold plating."),
("B","Use a network diagram (not a bar chart) to show interdependencies between activities."),
("D","Total float is the time an activity can slip without delaying the project completion date."),
("D","Float = LF - ES - duration = 18 - 2 - 5 = 11."),
("D","Use contingency reserve for the anticipated supplier delay, and find out how late the critical activity will be."),
("A","Choose the product with the lower life-cycle cost."),
("C","EV (and AC) cannot be assessed beyond the data date - that is the diagram error."),
("B","Cost risk means project costs could end up higher than planned."),
("D","How deliverables are verified and accepted is described in the scope management plan."),
("C","Defects found by the customer after delivery are external failure costs."),
("A","Saying quality planning is done 'only' during PM-plan development is false; it is iterative throughout."),
("D","A quality audit identifies inefficient and ineffective policies/processes."),
("D","Determining design variables for speed and safety uses design of experiments."),
("A","With huge volume and destructive testing, inspect a sample (statistical sampling)."),
("A","Borrowed resources reporting to functional managers, hard to motivate, hinder team building in a matrix."),
("D","With no reward/formal authority, the PM relies most effectively on expert power."),
("D","Assuming a great engineer will be a great PM is the halo effect."),
("C","Improving the physical work environment addresses Herzberg's hygiene factors."),
("B","The two team members should decide on the best course of action."),
("D","Feedback is part of effective communication, not a communication barrier."),
("D","A bar (Gantt) chart is best for reporting schedule status to the team during executing."),
("D","A sarcastic tone (pitch/tone conveying meaning) is paralingual communication."),
("A","Mary encoded the text, Tom decoded it and then encoded his feedback (phone call)."),
("C","Garbled, smudged text that interferes with the message is noise."),
("D","0.80 x $100,000 = $80,000 is the expected monetary value."),
("D","A newly discovered (not yet occurred) risk should first be qualified/analyzed."),
("D","Monitoring the weather and having a contingency plan would have prevented the data loss."),
("D","Gaining knowledge useful on future projects is a positive risk (opportunity)."),
("B","Secondary risks are new risks created by the risk responses you choose."),
("A","With experts dispersed and reachable only by email, the Delphi technique is best."),
("D","A data quality assessment checks how accurate and reliable risk data is before qualitative analysis."),
("C","A risk audit examines the effectiveness of risk responses (and the risk process)."),
("D","For a requirement dispute with a vendor, first refer to the procurement statement of work."),
("A","With no time/info for a detailed SOW and large effort, Time & Material is best."),
("B","At a bidder conference, put all questions and answers in writing and send them to all sellers."),
("C","If goods meet the need but not the contract, issue a change order to align the contract specifications."),
("B","Contracts should include procedures to accommodate changes."),
("C","A Fixed-Price contract puts the most cost risk on the seller (your company)."),
("D","Adding risks, requirements and stakeholders updates project documents, which do not need formal CCB approval."),
("C","Stakeholders have the most influence at the beginning of the project."),
("D","Facilitation helps draw consistent input from all stakeholders."),
("A","Desired engagement levels and how stakeholders are involved are in the stakeholder engagement plan."),
("D","Identify Stakeholders is an initiating process - you need stakeholders' requirements before planning."),
("B","A stakeholder register holds assessment and classification information about identified stakeholders."),
("D","A stakeholder's preferred communication method is captured in the stakeholder engagement plan/register."),
("D","A sponsor actively rallying others to support the project shows a Leading engagement level."),
("B","High interest / low power stakeholders should be kept informed."),
("A","Respectfully decline the expensive gift and return the tickets."),
("B","Business value is the net quantifiable benefit derived from a business endeavor."),
("A,B,C","A benefits management plan includes strategic alignment, metrics and target benefits (business need is in the business case)."),
("B","Company culture and organizational structure are the EEF to watch in Identify Stakeholders."),
("A","Market research gathers information on specific seller capabilities during Plan Procurement."),
("C","Aligning projects, programs and portfolios to strategy is organizational project management (OPM)."),
("D","Benefit-cost ratio is also known as cost-benefit analysis."),
("A","The payback period is the simplest and least precise selection method."),
("B","Honesty entails truthful reporting."),
("B","Full authority with a team outside the normal structure best fits a strong matrix (toward projectized)."),
("A","A 3-year, $1.5B undertaking is a megaproject (>$1B)."),
("C","The requirements traceability matrix links requirements to objectives."),
("A","A project-oriented (projectized) organization gives the PM high-to-total access to resources."),
("A,B,D","Project initiation drivers: compliance/legal/social needs, stakeholder requests, and improving products/processes."),
("B","A project halted by loss of funding ends by Starvation."),
("A,D","Org change management considers a framework for change and applying it at project/program/portfolio levels."),
("B","Choosing which processes fit the project is tailoring."),
("A","Setting strategic objectives and selecting projects is governance/portfolio work, not a typical PMO support role - that is the exception."),
("C","Evaluating proposals to best support company goals is portfolio management."),
("A","A proposal with market demand, ROI and cost analysis is a business case."),
("D","Expected business value and how it is measured are in the benefits management plan."),
("D","Whether the project is on track to deliver planned value is checked against the benefits management plan."),
("A","Auditing compliance with standards is quality assurance."),
("C","Governance frameworks are enterprise environmental factors."),
("C","A new PM should first assess the organization's culture to be effective."),
]

# Load the raw question data (JS literal)
qjs = open(os.path.join(BUILD, 'questions_data.js'), encoding='utf-8').read()

# Build ANSWERS JS literal
def js_escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

ans_lines = ['const ANSWERS = [']
for c, e in ANSWERS:
    letters = '[' + ','.join('"%s"' % x.strip() for x in c.split(',')) + ']'
    ans_lines.append('{c:%s,e:"%s"},' % (letters, js_escape(e)))
ans_lines.append('];')
ans_js = '\n'.join(ans_lines)

print('answers:', len(ANSWERS))

# ---- New question bank (from the 4 image docs), embedded as its own JS array ----
import sys
sys.path.insert(0, BUILD)
import new_questions
importlib_done = True
try:
    import importlib
    importlib.reload(new_questions)
except Exception:
    pass
NEW = new_questions.NEW

def js_str(s):
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"').replace('\r', '').replace('\n', '\\n') + '"'

new_lines = ['const NEW_RAW = [']
for e in NEW:
    opts = '[' + ','.join(js_str(o) for o in e['opts']) + ']'
    c = '[' + ','.join('"%s"' % x.strip() for x in e['c']) + ']'
    fields = 'src:%s,n:%d,q:%s,opts:%s,ans:{c:%s,e:%s},lang:%s' % (
        js_str(e['src']), int(e['n']), js_str(e['q']), opts, c,
        js_str(e['e']), js_str(e.get('lang', 'en')))
    if e.get('type', 'mcq') != 'mcq':
        fields += ',qtype:%s' % js_str(e['type'])
    new_lines.append('{' + fields + '},')
new_lines.append('];')
new_js = '\n'.join(new_lines)
print('new questions:', len(NEW))

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pass Your PMP - Practice Quiz</title>
<style>
:root{
  --bg:#0f1220; --card:#1a1f36; --card2:#232a4d; --text:#e8ebff; --muted:#9aa3c7;
  --accent:#6c8cff; --green:#2ecc71; --greenbg:#10351f; --red:#ff5d6c; --redbg:#3a1320;
  --border:#2c3360; --gold:#ffd166;
}
*{box-sizing:border-box}
body{margin:0;font-family:'Segoe UI',system-ui,Arial,sans-serif;background:linear-gradient(160deg,#0f1220,#161a33);color:var(--text);min-height:100vh}
header{padding:18px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:14px;flex-wrap:wrap;position:sticky;top:0;background:#10132475;backdrop-filter:blur(10px);z-index:10}
header h1{font-size:18px;margin:0;font-weight:700}
header .sub{color:var(--muted);font-size:13px}
.wrap{max-width:860px;margin:0 auto;padding:22px 16px 80px}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.pill{background:var(--card);border:1px solid var(--border);border-radius:999px;padding:6px 12px;font-size:13px;color:var(--muted)}
.pill b{color:var(--text)}
.progress{height:8px;background:var(--card);border-radius:999px;overflow:hidden;flex:1;min-width:140px}
.progress > i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),#9b6cff);width:0%}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px 20px 22px;box-shadow:0 10px 30px #0006}
.qmeta{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:12px;margin-bottom:10px}
.qtext{font-size:18px;line-height:1.5;margin:0 0 16px;font-weight:600}
.opts{display:flex;flex-direction:column;gap:10px}
.opt{display:flex;gap:12px;align-items:flex-start;text-align:left;background:var(--card2);border:1.5px solid var(--border);border-radius:12px;padding:13px 14px;cursor:pointer;color:var(--text);font-size:15px;line-height:1.4;transition:.15s;width:100%}
.opt:hover{border-color:var(--accent)}
.opt .lbl{font-weight:800;color:var(--accent);min-width:20px}
.opt.correct{background:var(--greenbg);border-color:var(--green)}
.opt.correct .lbl{color:var(--green)}
.opt.wrong{background:var(--redbg);border-color:var(--red)}
.opt.wrong .lbl{color:var(--red)}
.opt.disabled{cursor:default}
.opt .mark{margin-left:auto;font-weight:800}
.reveal{margin-top:16px;padding:15px;border-radius:12px;background:#0e1430;border:1px solid var(--border);display:none}
.reveal.show{display:block;animation:fade .25s}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1}}
.reveal .ans{font-weight:700;margin-bottom:6px}
.reveal .ans .ok{color:var(--green)}
.reveal .ans .no{color:var(--red)}
.reveal .exp{color:#c9d0f5;font-size:14.5px;line-height:1.55}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;border:0;border-radius:10px;padding:11px 16px;font-size:14px;font-weight:600;cursor:pointer;text-decoration:none}
.btn.ghost{background:transparent;border:1px solid var(--border);color:var(--text)}
.btn.gold{background:linear-gradient(90deg,#ff9e2c,#ffd166);color:#2a1a00}
button.btn:disabled{opacity:.4;cursor:default}
a.claude{text-decoration:none}
.nav{display:flex;justify-content:space-between;gap:10px;margin-top:18px}
.ar{direction:rtl;text-align:right;color:#b9c0e6;font-size:15px;line-height:1.6;margin-top:14px;padding-top:14px;border-top:1px dashed var(--border);display:none}
.ar.show{display:block}
.ar .aopt{padding:4px 0}
.toggle{font-size:12px;color:var(--muted);cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:6px}
.jump{display:flex;gap:8px;align-items:center}
.jump input{width:64px;background:var(--card2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:6px 8px;font-size:13px}
.hint{color:var(--muted);font-size:12.5px;margin-top:8px}
.badge{font-size:11px;padding:2px 8px;border-radius:999px;background:#2a325f;color:#c9d0f5}
.tabs{display:flex;gap:8px;margin-bottom:14px}
.tab{flex:1;background:var(--card);border:1px solid var(--border);color:var(--muted);border-radius:12px;padding:11px 14px;font-size:14px;font-weight:600;cursor:pointer;transition:.15s}
.tab:hover{border-color:var(--accent)}
.tab.active{background:linear-gradient(90deg,#26305c,#2f3a6e);color:var(--text);border-color:var(--accent)}
.tab b{color:var(--accent)}
.pkgbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 14px}
.pkgbar label{color:var(--muted);font-size:13px;font-weight:600}
.pkgbar select{background:var(--card2);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:8px 10px;font-size:13px;cursor:pointer;max-width:100%}
.pkgbar select:hover{border-color:var(--accent)}
.footer-note{color:var(--muted);font-size:12px;text-align:center;margin-top:24px;line-height:1.6}
.checkbtn{margin-top:12px}
@media(max-width:560px){.qtext{font-size:16px}.opt{font-size:14px}}
</style>
</head>
<body>
<header>
  <h1>📘 Pass Your PMP — Practice Quiz</h1>
  <span class="sub">Answer to reveal the correct one + explanation; questions you miss collect in ❌ Wrong for a focused retake</span>
</header>
<div class="wrap">
  <div class="tabs">
    <button class="tab active" data-set="orig">📘 Original · <b id="cnt-orig">0</b></button>
    <button class="tab" data-set="news">🆕 New set · <b id="cnt-news">0</b></button>
    <button class="tab" data-set="wrong">❌ Wrong · <b id="cnt-wrong">0</b></button>
  </div>
  <div id="pkgbar" class="pkgbar">
    <label for="pkgsel">📦 Package</label>
    <select id="pkgsel"></select>
  </div>
  <div class="bar">
    <div class="progress"><i id="pbar"></i></div>
    <span class="pill">Q <b id="qnum">1</b> / <b id="qtotal">0</b></span>
    <span class="pill">Score <b id="score">0</b>/<b id="answered">0</b></span>
    <span class="pill jump">Go to <input id="jumpin" type="number" min="1"> <button class="btn ghost" id="jumpbtn" style="padding:6px 10px">Go</button></span>
  </div>

  <div id="wrongctl" style="display:none;margin:0 0 12px;text-align:right">
    <button class="btn ghost" id="clearwrong" style="padding:6px 12px;font-size:13px">🗑 Clear wrong-answer list</button>
  </div>
  <div class="card" id="card"></div>

  <div class="nav">
    <button class="btn ghost" id="prev">← Previous</button>
    <button class="btn" id="next">Next →</button>
  </div>

  <div class="footer-note">
    Tip: After answering, click <b>“Analyze with Claude”</b> to open a chat that explains why the
    correct answer is right — and why your choice was right or wrong.<br>
    Answer key compiled for study practice; if anything looks off, the Claude analysis will clarify it.
  </div>
</div>

<script>
__QDATA__
__ADATA__
__NEWDATA__

// Two banks: the original slide deck, and the new set from the 4 image docs.
const ORIG = RAW_QUESTIONS.map((q,i)=>({...q, ans: ANSWERS[i], _set:'orig'}));
const NEWS = (typeof NEW_RAW!=='undefined'?NEW_RAW:[]).map(q=>({...q, _set:'new'}));
const SETS = { orig:{list:ORIG}, news:{list:NEWS}, wrong:{list:[]} };
const view = { orig:{idx:0,state:{},pkg:0}, news:{idx:0,state:{},pkg:0}, wrong:{idx:0,state:{}} };
let cur = 'orig';

// --- Study packages: split each bank into chunks of PKG questions ---
const BANKS = { orig:ORIG, news:NEWS };
const PKG = 45;
const clamp = (v,lo,hi)=> v<lo?lo : (v>hi?hi:v);
function pkgCount(set){ return Math.max(1, Math.ceil(BANKS[set].length / PKG)); }
function applyPackage(set){
  const p = clamp(view[set].pkg||0, 0, pkgCount(set)-1);
  view[set].pkg = p;
  SETS[set].list = BANKS[set].slice(p*PKG, p*PKG+PKG);   // slice keeps the same question object refs
}
function buildPkgSelector(){
  const bar = $('#pkgbar'), sel = $('#pkgsel');
  if(cur==='wrong'){ if(bar) bar.style.display='none'; return; }   // Wrong tab isn't packaged
  if(bar) bar.style.display='flex';
  const n = pkgCount(cur), full = BANKS[cur].length;
  sel.innerHTML='';
  for(let i=0;i<n;i++){
    const a=i*PKG+1, b=Math.min((i+1)*PKG, full);
    const o=document.createElement('option');
    o.value=i; o.textContent='Package '+(i+1)+' of '+n+' · Q'+a+'–'+b+' ('+(b-a+1)+')';
    sel.appendChild(o);
  }
  sel.value = String(view[cur].pkg||0);
}

// --- Remember the last set / package / position across sessions ---
function saveLast(){
  try{ localStorage.setItem('pmpLastV1', JSON.stringify({
    cur, pkg:{orig:view.orig.pkg, news:view.news.pkg}, idx:{orig:view.orig.idx, news:view.news.idx}
  })); }catch(e){}
}

// --- Wrong-answer review: accumulates across sessions via localStorage ---
const ALL = ORIG.concat(NEWS);
function hashStr(s){let h=0;for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0;}return h;}
function qSig(q){return q._set+'#'+(q._set==='orig'?('s'+q.slide):(q.src+'|'+q.n))+'#'+hashStr(q.q);}
let wrongKeys;
try{ wrongKeys = new Set(JSON.parse(localStorage.getItem('pmpWrongV1')||'[]')); }catch(e){ wrongKeys = new Set(); }
const _allSigs = new Set(ALL.map(qSig));
wrongKeys = new Set([...wrongKeys].filter(k=>_allSigs.has(k)));   // drop stale keys from older builds
function saveWrong(){ try{ localStorage.setItem('pmpWrongV1', JSON.stringify([...wrongKeys])); }catch(e){} }
function rebuildWrong(){ SETS.wrong.list = ALL.filter(q=>wrongKeys.has(qSig(q))); }
function markResult(q,isCorrect){
  const k=qSig(q);
  if(isCorrect){ if(wrongKeys.has(k)){ wrongKeys.delete(k); saveWrong(); updateCounts(); } }
  else if(!wrongKeys.has(k)){ wrongKeys.add(k); saveWrong(); updateCounts(); }
}
function updateCounts(){ const e=$('#cnt-wrong'); if(e) e.textContent = wrongKeys.size; }

const $ = s=>document.querySelector(s);
const card = $('#card');

function letters(n){return 'ABCDE'.slice(0,n).split('');}

// Condensed persona of the pmp-expert skill, so the analysis works on claude.ai too.
const SKILL_INTRO =
`Act as my PMP exam coach using the "pmp-expert" skill mindset (if you have that skill available, use it). \
Analyze through the PMI mindset: favor servant leadership; the PM solves problems at their level before escalating to sponsor/PMO/management; \
understand the root cause before acting; be proactive not reactive; resolve conflict by collaborating (win-win) and talk to people directly; \
follow change control and never gold-plate or add scope informally; a deliverable is complete only on formal documented customer acceptance; \
in agile/hybrid the team self-organizes and estimates while the PM facilitates and removes impediments. \
When two options both look right, choose the most proactive, collaborative, root-cause option over escalating, blaming, delaying, or merely documenting.`;

function claudePrompt(q, picked, correctLetters){
  const L = letters(q.opts.length);
  let opt = q.opts.map((o,i)=>L[i]+') '+o).join('\n');
  const pickStr = picked.length ? picked.join(', ') : '(none)';
  return `${SKILL_INTRO}

Now analyze this PMP practice question for me.

QUESTION:
${q.q}

OPTIONS:
${opt}

The answer key says the correct answer is: ${correctLetters.join(', ')}
I chose: ${pickStr}

Follow this analysis protocol:
1) State the correct answer and the PMI reasoning that makes it right.
2) Tell me whether my choice was right or wrong — if wrong, name the distractor trap I fell for.
3) One crisp line on why each other option is wrong.
4) The key takeaway to remember, and which ECO domain it belongs to (People / Process / Business Environment).
If the answer key looks wrong, say so and give the PMI-correct answer.`;
}
function claudeURL(q, picked, correctLetters){
  return 'https://claude.ai/new?q=' + encodeURIComponent(claudePrompt(q, picked, correctLetters));
}
function copyText(t){
  try { navigator.clipboard.writeText(t); return true; } catch(e){}
  try {
    const ta=document.createElement('textarea');
    ta.value=t; ta.style.position='fixed'; ta.style.opacity='0';
    document.body.appendChild(ta); ta.focus(); ta.select();
    document.execCommand('copy'); document.body.removeChild(ta);
    return true;
  } catch(e){ return false; }
}

function render(){
  const S = SETS[cur], V = view[cur];
  const list = S.list, state = V.state, N = list.length;
  if(N===0){
    card.innerHTML = (cur==='wrong')
      ? `<p class="qtext">No wrong answers saved yet 🎉</p>
         <p class="hint">Answer questions in the 📘 Original or 🆕 New set tabs. Any you miss collect here so you can retake just those — and getting one right here removes it from the list.</p>`
      : `<p class="qtext">No questions in this set yet.</p>
         <p class="hint">This bank is still being added. Switch to the other tab above.</p>`;
    updateBar(); return;
  }
  if(V.idx>=N) V.idx = N-1;
  const idx = V.idx;
  const q = list[idx];
  const L = letters(q.opts.length);
  const multi = q.ans.c.length > 1;
  const rtl = q.lang==='ar';
  const st = state[idx] || (state[idx] = {picked:new Set(), done:false, correct:false});

  let optsHtml = q.opts.map((o,i)=>{
    const ltr = L[i];
    let cls = 'opt';
    let mark = '';
    if(st.done){
      cls += ' disabled';
      const isCorrect = q.ans.c.includes(ltr);
      const wasPicked = st.picked.has(ltr);
      if(isCorrect){cls+=' correct'; mark='✓';}
      else if(wasPicked){cls+=' wrong'; mark='✗';}
    }
    return `<button class="${cls}" data-l="${ltr}"${rtl?' dir="rtl" style="text-align:right"':''}>
      <span class="lbl">${ltr}</span><span>${o}</span>
      <span class="mark">${mark}</span></button>`;
  }).join('');

  const correctStr = q.ans.c.join(', ');
  let revealCls = st.done ? 'reveal show' : 'reveal';
  let resultLine = '';
  if(st.done){
    resultLine = st.correct
      ? `<span class="ok">✓ Correct!</span>`
      : `<span class="no">✗ Not quite.</span> Correct answer: <b>${correctStr}</b>`;
  }

  const fromOrig = q._set==='orig';
  const metaLeft = fromOrig
    ? `Question ${idx+1} of ${N} &nbsp;·&nbsp; <span class="badge">slide ${q.slide}</span>`
    : `Question ${idx+1} of ${N} &nbsp;·&nbsp; <span class="badge">${q.src} · #${q.n}</span>`;
  const metaRight = (fromOrig && q.aq)
    ? `<span class="toggle" id="artog">🌐 العربية</span>` : '';

  card.innerHTML = `
    <div class="qmeta">
      <span>${metaLeft}</span>
      ${metaRight}
    </div>
    <p class="qtext"${rtl?' dir="rtl" style="text-align:right"':''}>${q.q}</p>
    ${multi ? `<div class="hint">Multiple answers — select ${q.ans.c.length}, then press <b>Check answer</b>.</div>`:''}
    <div class="opts" id="opts">${optsHtml}</div>
    ${multi && !st.done ? `<button class="btn checkbtn" id="checkbtn">Check answer</button>`:''}
    <div class="${revealCls}" id="reveal">
      <div class="ans">${resultLine}</div>
      <div class="exp"${rtl?' dir="rtl" style="text-align:right"':''}>${q.ans.e}</div>
      <div class="actions">
        <a class="btn gold" id="claudelink" href="#" target="_blank" rel="noopener">✨ Analyze with Claude</a>
      </div>
    </div>
    ${(fromOrig && q.aq) ? `<div class="ar" id="arbox">
        <div><b>${q.aq}</b></div>
        ${(q.aopts||[]).map((o,i)=>`<div class="aopt">${L[i]}) ${o}</div>`).join('')}
      </div>`:''}
  `;

  document.querySelectorAll('#opts .opt').forEach(b=>{
    b.addEventListener('click',()=>{
      if(st.done) return;
      const l = b.dataset.l;
      if(multi){
        if(st.picked.has(l)){st.picked.delete(l); b.classList.remove('correct');}
        else{st.picked.add(l); b.classList.add('correct');}
      } else {
        st.picked = new Set([l]);
        commit();
      }
    });
  });
  const cb = document.getElementById('checkbtn');
  if(cb) cb.addEventListener('click',()=>{ if(st.picked.size) commit(); });

  const artog = document.getElementById('artog');
  if(artog) artog.addEventListener('click',()=>{
    const box = document.getElementById('arbox');
    if(box) box.classList.toggle('show');
  });

  if(st.done) wireClaude();

  function commit(){
    st.done = true;
    const pickedArr = [...st.picked].sort();
    const correctArr = [...q.ans.c].sort();
    st.correct = pickedArr.length===correctArr.length && pickedArr.every((v,i)=>v===correctArr[i]);
    markResult(q, st.correct);
    render();
  }
  function wireClaude(){
    const link = document.getElementById('claudelink');
    if(!link) return;
    const text = claudePrompt(q, [...st.picked], q.ans.c);
    link.href = 'https://claude.ai/new?q=' + encodeURIComponent(text);
    link.addEventListener('click', ()=>{ copyText(text); });
  }

  updateBar();
}

function updateBar(){
  const S = SETS[cur], V = view[cur], N = S.list.length;
  $('#qnum').textContent = N ? (V.idx+1) : 0;
  $('#qtotal').textContent = N;
  $('#jumpin').max = N;
  $('#pbar').style.width = (N ? ((V.idx+1)/N*100) : 0)+'%';
  $('#prev').disabled = N===0 || V.idx===0;
  $('#next').disabled = N===0 || V.idx>=N-1;
  let s=0,a=0;
  for(const k in V.state){ if(V.state[k].done){a++; if(V.state[k].correct)s++;} }
  $('#score').textContent=s; $('#answered').textContent=a;
  const wc=$('#wrongctl'); if(wc) wc.style.display = (cur==='wrong' && wrongKeys.size) ? 'block':'none';
}

// Tab switching
document.querySelectorAll('.tab').forEach(t=>{
  t.addEventListener('click',()=>{
    cur = t.dataset.set;
    if(cur==='wrong'){ rebuildWrong(); view.wrong = {idx:0,state:{}}; }   // fresh retake of the current wrong list
    else { applyPackage(cur); }
    document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active', x===t));
    buildPkgSelector(); saveLast(); render();
  });
});
$('#cnt-orig').textContent = ORIG.length;
$('#cnt-news').textContent = NEWS.length;
updateCounts();

$('#clearwrong').onclick=()=>{
  if(!wrongKeys.size) return;
  if(confirm('Clear all '+wrongKeys.size+' saved wrong answers? This cannot be undone.')){
    wrongKeys.clear(); saveWrong(); updateCounts(); rebuildWrong();
    view.wrong = {idx:0,state:{}}; render();
  }
};

$('#pkgsel').addEventListener('change',()=>{
  view[cur].pkg = parseInt($('#pkgsel').value,10)||0;
  view[cur].idx = 0; view[cur].state = {};     // fresh start within the chosen package
  applyPackage(cur); saveLast(); render();
});
$('#prev').onclick=()=>{ const V=view[cur]; if(V.idx>0){V.idx--;saveLast();render();} };
$('#next').onclick=()=>{ const V=view[cur]; if(V.idx<SETS[cur].list.length-1){V.idx++;saveLast();render();} };
$('#jumpbtn').onclick=()=>{
  const N=SETS[cur].list.length; let v=parseInt($('#jumpin').value,10);
  if(v>=1&&v<=N){view[cur].idx=v-1;saveLast();render();}
};
$('#jumpin').addEventListener('keydown',e=>{ if(e.key==='Enter')$('#jumpbtn').click(); });
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='INPUT')return;
  if(e.key==='ArrowRight')$('#next').click();
  if(e.key==='ArrowLeft')$('#prev').click();
});

// --- Initialize packages, then restore the last session ---
applyPackage('orig'); applyPackage('news');
(function restoreLast(){
  let last=null; try{ last = JSON.parse(localStorage.getItem('pmpLastV1')||'null'); }catch(e){}
  if(!last) return;
  if(last.pkg){
    view.orig.pkg = clamp(last.pkg.orig|0, 0, pkgCount('orig')-1);
    view.news.pkg = clamp(last.pkg.news|0, 0, pkgCount('news')-1);
    applyPackage('orig'); applyPackage('news');
  }
  if(['orig','news','wrong'].indexOf(last.cur)>=0) cur = last.cur;
  if(last.idx){
    view.orig.idx = clamp(last.idx.orig|0, 0, SETS.orig.list.length-1);
    view.news.idx = clamp(last.idx.news|0, 0, SETS.news.list.length-1);
  }
})();
if(cur==='wrong'){ rebuildWrong(); view.wrong={idx:0,state:{}}; }
document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active', t.dataset.set===cur));
buildPkgSelector();
render();
</script>
</body>
</html>
'''

html = (HTML.replace('__QDATA__', qjs)
            .replace('__ADATA__', ans_js)
            .replace('__NEWDATA__', new_js)
            .replace('__N__', str(len(ANSWERS))))

targets = [
    os.path.join(OUT, 'index.html'),
    os.path.join(REPO_ROOT, 'index.html'),
    os.path.join(SITE_DEPLOY, 'index.html'),
]
for target in targets:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', target)
print('questions in data:', qjs.count('{slide:'))
