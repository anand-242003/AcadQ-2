"""Resources Discovery page."""
import streamlit as st

def _render_topbar():
    """Fixed top app bar."""
    st.markdown('<div style="position:fixed;top:0;left:0;right:0;z-index:9999;height:64px;display:flex;align-items:center;justify-content:space-between;padding:0 5%;background:rgba(250,249,247,.92);backdrop-filter:blur(20px);border-bottom:1px solid rgba(218,192,196,.15);font-family:Manrope,sans-serif"><div style="display:flex;align-items:center;gap:32px"><a href="/?p=dash" style="text-decoration:none;display:flex;align-items:center;gap:12px;transition:opacity .2s" onmouseover="this.style.opacity=.8" onmouseout="this.style.opacity=1"><span style="font-size:22px;font-weight:900;color:#6e1a37;letter-spacing:-0.5px">AcadIQ</span><span style="width:1px;height:20px;background:rgba(218,192,196,.3);display:inline-block"></span><span style="font-size:14px;font-weight:700;color:#510122">Resources</span></a><div style="display:flex;gap:24px;margin-left:16px"><a href="/?p=dash" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Predictor</a><a href="/?p=plan" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Study Plan</a><a href="/?p=quiz" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">Quiz Bot</a><a href="/?p=coach" style="text-decoration:none;font-size:13px;font-weight:600;color:#544246;font-family:Inter,sans-serif;opacity:.8" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=.8">AI Coach</a></div></div></div><div style="height:80px"></div>', unsafe_allow_html=True)


def show_resources():
    """Render the academic resource library."""
    _render_topbar()

    st.markdown('<h1 style="font-family:Manrope,sans-serif;font-size:34px;font-weight:900;color:#1a1c1b;letter-spacing:-1px;margin:0 0 4px 0">Intelligence Library</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#544246;font-size:14px;font-weight:500;margin-bottom:32px">Academic resources automatically curated to supplement your study plan and prediction weaknesses.</p>', unsafe_allow_html=True)

    from pathlib import Path
    import base64


    resources = st.session_state.get("plan_resources", [])


    MEANINGFUL_EXTRACTS = {
        "Cepeda2006": """the item to be unrecoverable; see Pashler et al., 2005) This feed- back hypothesis is supported by a single study (Cull, Shaughnessy, & Zechmeister, 1996). Unfortunately, the feedback hypothesis cannot be tested adequately with current data, because all three of the studies using (page 12)""",
        "Procrastination_2": """itchell, 1997) and thus can offer only limited contributions. Consequently, there is much interesting work to be done in the scientific fundamentals of description, prediction, and control. To begin with, although this review strongly indicates that TMT provides an excellent desc (page 19)""",
        "Stickgold&Walker_Sleep Medicine_2007": """ntegration/association) [20,21], the develop- ment of hippocampal independence for declarative Reactivation Destabilize Reconsolidate Memoryformation 1 -50d 02 h 4 h 6 h 2 4 h Deteriorate 50ms 5s 15min 6h 10yr 1yr1wk Encode Stabilize Enhance Integrate HC-independence Fig. 2. Time (page 3)""",
        "science.1199327.full_": """/ www.sciencexpress.org / 20 January 2011 / Page 1 / 10.1126/science.1199327 Educators rely heavily on learning activities that encourage elaborative studying, while activities that require students to practice retrieving and reconstructing knowledge are used less frequently. Here, we show that practicing retrieval produces greater gains in meaningful learning than elaborative studying with concept mapping.""",
        "Zimmerman-B.-2002-Becoming-Self-Regulated-Learner": """Becoming a Self-Regulated Learner: An Overview Barry J. Zimmerman. Self-regulation is not a mental ability or an academic performance skill; rather it is the self-directive process by which learners transform their mental abilities into academic skills.""",
        "dunloskiimprovingstudentlearning": """Improving Students’ Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology. Fortunately, cognitive and educational psychologists have been developing and evaluating easy-to-use learning techniques that could help students achieve their learning goals.""",
        "Dweck 2008 Transforming Students’ Motivation to Learn": """Transforming Students’ Motivation to Learn Carol S. Dweck. we have shown that what students believe about their brains — whether they see their intelligence as something that's fixed or something that can grow and change — has profound effects on their motivation, learning, and school achievement. These different beliefs, or mindsets, create different psychological worlds.""",
        "Sweller - 1988 - Cognitive load during problem solving (1)": """Considerable evidence indicates that domain specific knowledge in the form of schemes is the primary factor distinguishing experts from novices in problem-solving skill. Conventional problem solving in the form of means-ends analysis requires a relatively large amount of cognitive processing capacity."""
    }

    RESOURCE_WEB_URLS = {
        "dunloskiimprovingstudentlearning": "https://www.whz.de/fileadmin/lehre/hochschuldidaktik/docs/dunloskiimprovingstudentlearning.pdf",
        "science.1199327.full_": "https://www.bates.edu/research/files/2018/07/science.1199327.full_.pdf",
        "Cepeda2006": "https://augmentingcognition.com/assets/Cepeda2006.pdf",
        "Sweller - 1988 - Cognitive load during problem solving (1)": "https://andymatuschak.org/files/papers/Sweller%20-%201988%20-%20Cognitive%20load%20during%20problem%20solving.pdf",
        "Zimmerman-B.-2002-Becoming-Self-Regulated-Learner": "https://www.leiderschapsdomeinen.nl/wp-content/uploads/2016/12/Zimmerman-B.-2002-Becoming-Self-Regulated-Learner.pdf",
        "Procrastination_2": "https://studypedia.au.dk/fileadmin/www.studiemetro.au.dk/Procrastination_2.pdf",
        "Dweck 2008 Transforming Students’ Motivation to Learn": "https://www.rpforschools.net/articles/Mindsets/Dweck%202008%20Transforming%20Students%E2%80%99%20Motivation%20to%20Learn.pdf",
        "Stickgold&Walker_Sleep Medicine_2007": "https://walkerlab.berkeley.edu/reprints/Stickgold&Walker_Sleep%20Medicine_2007.pdf",
        "Learning_And_Memory_Under_Stress": "https://www.researchgate.net/publication/304572997_Learning_and_memory_under_stress_implications_for_the_classroom"
    }

    if not resources:
        RES_DIR = Path("backend/data/resoureces")
        if RES_DIR.exists():
            pdfs = list(RES_DIR.glob("*.pdf"))
            for p in pdfs:
                resources.append({
                    "title": p.stem.replace("_", " "),
                    "url": p.name
                })


        resources.append({
            "title": "Learning and Memory Under Stress",
            "topic": "Cognitive Science",
            "description": "Implications for the classroom and student performance under pressure.",
            "url": "Learning_And_Memory_Under_Stress"
        })

    if not resources:
        st.info("No resource files found in backend/data/resoureces.")
        return


    RES_DIR = Path("backend/data/resoureces")
    for r in resources:
        url = r.get("url", "")
        stem = Path(url).stem if url else r.get("title", "").replace(" ", "_")

        if not r.get("topic"):
            r["topic"] = "Cognitive Science" if "cognitive" in stem.lower() or "sweller" in stem.lower() else ("Wellness" if "sleep" in stem.lower() else "Research Paper")

        if not r.get("file_path") and url:
            p = RES_DIR / url
            if p.exists():
                r["file_path"] = str(p)

        if not r.get("extract"):
            r["extract"] = MEANINGFUL_EXTRACTS.get(stem, "")
            if not r["extract"] and r.get("file_path"):
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(r["file_path"])
                    if len(reader.pages) > 0:
                        text = reader.pages[0].extract_text()
                        r["extract"] = text[:1500] + "..." if len(text) > 1500 else text
                except Exception:
                    r["extract"] = "PDF extraction unavailable."

    for r in resources:
        url = r.get("url", "")
        stem = Path(url).stem if url else r.get("title", "").replace(" ", "_")
        web_link = RESOURCE_WEB_URLS.get(stem)

        st.markdown(f'<div style="background:#fff;border-radius:20px;padding:32px;border:1px solid rgba(218,192,196,.15);margin-top:24px;box-shadow:0 8px 24px rgba(81,1,34,.03);display:flex;align-items:flex-start;gap:20px"><div style="width:50px;height:50px;border-radius:14px;background:rgba(167,241,222,.2);display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0">📚</div><div><div style="display:flex;align-items:center;gap:12px;margin-bottom:8px"><h3 style="font-family:Manrope,sans-serif;font-size:18px;font-weight:800;color:#510122;margin:0">{r.get("title", "Resource")}</h3><span style="font-size:10px;font-weight:800;color:#1b6a5b;background:rgba(27,106,91,.1);padding:4px 10px;border-radius:99px;text-transform:uppercase;letter-spacing:1px">{r.get("topic", "Material")}</span></div><p style="font-size:13.5px;color:#544246;margin:0;line-height:1.6">{r.get("description", "")}</p></div></div>', unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            if r.get("extract"):
                with st.expander("Read Extract"):
                    st.write(r["extract"])
        with c2:
            if web_link:

                st.markdown(f'<a href="{web_link}" target="_blank" style="background:#510122;color:#fff;text-decoration:none;font-size:12px;font-weight:700;padding:8px 16px;border-radius:10px;display:inline-block;margin-top:8px;text-align:center;width:100%">Open Full Resource</a>', unsafe_allow_html=True)
            elif r.get("file_path"):

                with open(r["file_path"], "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_link = f'<a href="data:application/pdf;base64,{base64_pdf}" target="_blank" style="background:#510122;color:#fff;text-decoration:none;font-size:12px;font-weight:700;padding:8px 16px;border-radius:10px;display:inline-block;margin-top:8px;text-align:center;width:100%">Open Full PDF</a>'
                    st.markdown(pdf_link, unsafe_allow_html=True)
