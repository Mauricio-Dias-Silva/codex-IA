import json
import os
import sys
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Add parent directory to path for codex_ia imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_codex_agent():
    """Initialize and return the Codex Agent."""
    try:
        from codex_ia.core.agent import CodexAgent
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return CodexAgent(project_dir=project_dir)
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return None


# ============== PAGE VIEWS ==============

def dashboard(request):
    """Main dashboard view."""
    return render(request, 'core/dashboard.html', {
        'active_page': 'dashboard',
        'title': 'Codex-IA | Dashboard'
    })


def chat_view(request):
    """Chat with AI view."""
    return render(request, 'core/chat.html', {
        'active_page': 'chat',
        'title': 'Codex-IA | Chat'
    })


def missions_view(request):
    """Squad missions view."""
    return render(request, 'core/missions.html', {
        'active_page': 'missions',
        'title': 'Codex-IA | Missions'
    })


def night_shift_view(request):
    """Night shift (auto-improvement) view."""
    return render(request, 'core/night_shift.html', {
        'active_page': 'night_shift',
        'title': 'Codex-IA | Night Shift'
    })


def hunter_view(request):
    """Trend Hunter view."""
    return render(request, 'core/hunter.html', {
        'active_page': 'hunter',
        'title': 'Codex-IA | The Hunter'
    })


def council_view(request):
    """Council of AIs view."""
    return render(request, 'core/council.html', {
        'active_page': 'council',
        'title': 'Codex-IA | The Council'
    })


# ============== API ENDPOINTS ==============

@csrf_exempt
@require_POST
def api_chat(request):
    """API endpoint for chat with AI."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        agent = get_codex_agent()
        if agent:
            response = agent.chat(message)
            return JsonResponse({'response': response})
        else:
            # Fallback if agent not available
            return JsonResponse({
                'response': f"🤖 Codex-IA recebeu: '{message}'\n\n*Nota: Agente não inicializado. Configure GEMINI_API_KEY no .env*"
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_mission(request):
    """API endpoint for squad missions."""
    try:
        data = json.loads(request.body)
        mission = data.get('mission', '')
        
        if not mission:
            return JsonResponse({'error': 'Mission is required'}, status=400)
        
        try:
            from codex_ia.core.squad import SquadLeader
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            squad = SquadLeader(project_dir)
            result = squad.assign_mission(mission, apply=True, autopilot=True)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({
                'result': f"🚀 Missão recebida: '{mission}'\n\n*Erro ao executar: {e}*"
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_night_shift(request):
    """API endpoint for night shift auto-improvement."""
    try:
        try:
            from codex_ia.core.evolution_agent import EvolutionAgent
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            evo = EvolutionAgent(project_dir)
            result = evo.introspect()
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({
                'result': f"🌙 Night Shift iniciado...\n\n*Erro: {e}*"
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_hunter(request):
    """API endpoint for trend hunting."""
    try:
        try:
            from codex_ia.core.trend_hunter import TrendHunterAgent
            hunter = TrendHunterAgent()
            opportunities = hunter.scan_for_opportunities()
            return JsonResponse({'opportunities': opportunities})
        except Exception as e:
            return JsonResponse({
                'opportunities': [{
                    'title': 'Oportunidade Demo',
                    'description': f'Hunter não disponível: {e}',
                    'revenue': 'N/A',
                    'confidence': 0
                }]
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_parallel_chat(request):
    """API endpoint for PARALLEL AI processing."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        max_workers = data.get('max_workers', None)  # Limitar número de IAs
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        try:
            from codex_ia.core.brain_router import BrainRouter
            router = BrainRouter()
            result = router.parallel_execution(message, max_workers=max_workers)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e),
                'active_ais': [],
                'partial_results': {},
                'synthesis': f'Erro ao executar: {e}'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def api_council(request):
    """API endpoint for council of AIs."""
    try:
        data = json.loads(request.body)
        topic = data.get('topic', '')
        
        if not topic:
            return JsonResponse({'error': 'Topic is required'}, status=400)
        
        agent = get_codex_agent()
        if agent and hasattr(agent, 'llm_client'):
            result = agent.llm_client.council_meeting(topic)
            return JsonResponse({'result': result})
        else:
            return JsonResponse({
                'result': f"🗣️ O Conselho deliberou sobre: '{topic}'\n\n*Agente não disponível*"
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
