import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List

DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F8FAFC", family="Inter, system-ui, sans-serif"),
    margin=dict(l=30, r=30, t=40, b=30),
)


def render_radar_chart(skill_data: Dict[str, Dict[str, Any]]) -> go.Figure:
    """Create an interactive Plotly radar chart displaying evidence score vs coverage."""
    categories = list(skill_data.keys())
    if not categories:
        categories = ["Python", "Machine Learning", "System Design"]
        scores = [0, 0, 0]
        coverages = [0, 0, 0]
    else:
        scores = [skill_data[k].get("score", 0) for k in categories]
        coverages = [skill_data[k].get("coverage", 0) for k in categories]

    # Close the radar loop
    categories_closed = categories + [categories[0]]
    scores_closed = scores + [scores[0]]
    coverages_closed = coverages + [coverages[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(25, 199, 181, 0.35)',
        line=dict(color='#19C7B5', width=3),
        name='Evidence Score',
        hoverinfo='theta+r'
    ))

    fig.add_trace(go.Scatterpolar(
        r=coverages_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(167, 243, 208, 0.25)',
        line=dict(color='#A7F3D0', width=2, dash='dot'),
        name='Evidence Coverage (%)',
        hoverinfo='theta+r'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#A5ABB5", size=10),
                gridcolor="#343A44",
                linecolor="#343A44"
            ),
            angularaxis=dict(
                tickfont=dict(color="#F4F5F7", size=12, family="Inter, sans-serif"),
                gridcolor="#343A44",
                linecolor="#343A44"
            ),
            bgcolor="rgba(32, 36, 43, 0.6)"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color="#F8FAFC")
        ),
        **DARK_LAYOUT
    )
    return fig


def render_skill_bars(skill_data: Dict[str, Dict[str, Any]]) -> go.Figure:
    """Create a paired horizontal bar chart showing Evidence Score vs Coverage."""
    skills = list(skill_data.keys())
    scores = [skill_data[k].get("score", 0) for k in skills]
    coverages = [skill_data[k].get("coverage", 0) for k in skills]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=skills,
        x=scores,
        name='Score (out of 100)',
        orientation='h',
        marker=dict(
            color='#19C7B5',
            line=dict(color='#A7F3D0', width=1)
        ),
        text=scores,
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        y=skills,
        x=coverages,
        name='Code Coverage (%)',
        orientation='h',
        marker=dict(
            color='#292F38',
            line=dict(color='#343A44', width=1)
        ),
        text=coverages,
        textposition='inside'
    ))

    fig.update_layout(
        barmode='group',
        xaxis=dict(
            range=[0, 105],
            gridcolor="#343A44",
            tickfont=dict(color="#A5ABB5")
        ),
        yaxis=dict(
            tickfont=dict(color="#F4F5F7", size=12),
            gridcolor="rgba(0,0,0,0)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#F8FAFC")
        ),
        **DARK_LAYOUT
    )
    return fig


def render_evidence_pie(breakdown: Dict[str, List[str]]) -> go.Figure:
    """Donut chart for Observed Evidence vs AI Inference vs Missing Evidence."""
    labels = ["Observed Evidence", "AI Inference", "Missing Evidence"]
    counts = [
        len(breakdown.get("observed_evidence", [])),
        len(breakdown.get("ai_generated_inference", [])),
        len(breakdown.get("missing_evidence", []))
    ]
    colors = ["#10B981", "#8B5CF6", "#F59E0B"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=counts,
        hole=.55,
        marker=dict(colors=colors, line=dict(color='#0B0F19', width=2)),
        textinfo='label+value',
        textfont=dict(color="#F8FAFC", size=11),
    )])

    fig.update_layout(
        showlegend=False,
        **DARK_LAYOUT
    )
    return fig


def render_confusion_matrix_chart(matrix: List[List[int]], labels: List[str]) -> go.Figure:
    """Heatmap rendering for evaluation benchmark confusion matrix."""
    z = matrix
    annotations = []
    for i, row in enumerate(z):
        for j, val in enumerate(row):
            annotations.append(
                dict(
                    x=labels[j],
                    y=labels[i],
                    text=f"<b>{val}</b>",
                    showarrow=False,
                    font=dict(color="#FFFFFF", size=18)
                )
            )

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=labels,
        y=labels,
        colorscale=[[0, "#20242B"], [0.5, "#15B3A2"], [1, "#19C7B5"]],
        showscale=False
    ))

    fig.update_layout(
        annotations=annotations,
        xaxis=dict(
            title=dict(text="Predicted Classification", font=dict(color="#94A3B8")),
            tickfont=dict(color="#F8FAFC"),
        ),
        yaxis=dict(
            title=dict(text="Ground Truth", font=dict(color="#94A3B8")),
            tickfont=dict(color="#F8FAFC"),
            autorange="reversed",
        ),
        **DARK_LAYOUT
    )
    return fig
