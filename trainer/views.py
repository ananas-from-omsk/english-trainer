from django.shortcuts import render, redirect
from .models import Word
import random
from django.db.models import F
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Cast

def home(request):
    words = Word.objects.all()
    return render(request, 'trainer/home.html', {'words': words})

MAX_PROGRESS = 10

def train(request):
    mode = request.GET.get("mode", "all")

    if mode == "hard":
        words_qs = Word.objects.filter(wrong_answers__gte=3)
    else:
        words_qs = Word.objects.all()

    words = list(words_qs)

    if not words:
        return render(request, "trainer/train.html", {"word": None})

    progress = request.session.get("progress", 0)
    finished = progress >= 10

    result = None
    wrong_translation = None
    answered = False

    # ================= POST =================
    if request.method == "POST" and not finished:
        word_id = int(request.POST.get("word_id"))
        user_answer = request.POST.get("answer", "")

        word = Word.objects.get(id=word_id)

        wrong_translation = word.russian
        answered = True

        if user_answer.strip().lower() == word.russian.strip().lower():
            result = "correct"
            word.correct_answers += 1
            progress += 1
            request.session["progress"] = progress
        else:
            result = "wrong"
            word.wrong_answers += 1

        word.save()

    # ================= АДАПТИВНЫЙ ВЕС ПО ПРОЦЕНТУ =================
    weights = []

    for w in words:
        total = w.correct_answers + w.wrong_answers

        if total == 0:
            error_rate = 0
        else:
            error_rate = w.wrong_answers / total

        # базовый вес
        weight = 1

        # если ошибка > 30% → увеличиваем шанс
        if error_rate > 0.3:
            weight += error_rate * 5   # усиление

        weights.append(weight)

    word = random.choices(words, weights=weights, k=1)[0]

    return render(request, "trainer/train.html", {
        "word": None if finished else word,
        "result": result,
        "wrong_translation": wrong_translation,
        "progress": progress,
        "answered": answered,
        "finished": finished,
        "mode": mode,
    })

def get_weighted_word(words):
    weighted_list = []

    for word in words:
        # базовый вес
        weight = 1

        # если ошибался — увеличиваем шанс
        weight += word.wrong_answers * 3

        # если правильно отвечал — уменьшаем шанс
        weight -= word.correct_answers * 1

        # минимум 1, чтобы не исчезло
        weight = max(weight, 1)

        weighted_list.extend([word] * weight)

    return random.choice(weighted_list)

def reset_train(request):
    request.session["progress"] = 0
    return redirect("train")



def stats(request):
    words = Word.objects.all()

    data = []

    for w in words:
        total = w.correct_answers + w.wrong_answers

        if total > 0:
            percent = round((w.correct_answers / total) * 100)
        else:
            percent = None  # важно!

        data.append({
            "word": w,
            "correct": w.correct_answers,
            "wrong": w.wrong_answers,
            "percent": percent,
            "is_new": total == 0
        })

    # новые вниз
    data.sort(key=lambda x: (x["is_new"], -(x["percent"] or 0)))

    return render(request, "trainer/stats.html", {
        "data": data
    })
