@csrf_exempt
@require_POST
def api_generate_image(request):
    """API endpoint para geração de imagens com DALL-E + fallback Stable Diffusion."""
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        
        if not prompt:
            return JsonResponse({'error': 'Prompt é obrigatório'}, status=400)
        
        try:
            from codex_ia.core.image_generator import ImageGenerator
            generator = ImageGenerator()
            result = generator.generate(prompt)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e)
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
