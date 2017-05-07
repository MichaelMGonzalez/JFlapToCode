{%- extends "UnitySimple.jinja.cs" %}
{% block extra_functions %}
    {{super()}}
    protected void SetSecondsPerStep() {
        secondsPerStep = 1.0f/updateRate;
    }
    protected virtual void Start() {
        SetSecondsPerStep();
    }
    protected virtual void OnValidate() {
        SetSecondsPerStep();
    }
    protected void Update() {
        if( Time.time - timeLastTicked > secondsPerStep ) {
             Step();
        }
    }
{% endblock %}
{% block variables %}
    {{super()}}
    public int updateRate = 60;
    protected float timeLastTicked = 0;
    private float secondsPerStep;
{% endblock %}
