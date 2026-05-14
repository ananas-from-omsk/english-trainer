"""Views for English trainer app"""

import random

from django.shortcuts import render, redirect

from .models import Word
from .forms import WordForm


MAX_PROGRESS = 10


def home(request):
    """Главная страница со списком слов"""
    words = Word.objects.all()
    return render(request, 'trainer/home.html', {'words': words})


def train(request):
    """Тренировка слов"""

    mode = request.GET.get("mode", "all")

    if mode == "hard":
        words_qs = Word.objects.filter(wrong_answers__gte=3)
    else:
        words_qs = Word.objects.all()

    words = list(words_qs)

    if not words:
        return render(request, "trainer/train.html", {"word": None})

    progress = request.session.get("progress", 0)
    finished = progress >= MAX_PROGRESS

    result = None
    wrong_translation = None
    answered = False

    if request.method == "POST" and not finished:
        word_id = int(request.POST.get("word_id"))
        word = Word.objects.get(id=word_id)

        result, wrong_translation = process_answer(request, word)
        answered = True

        if result == "correct":
            progress += 1
            request.session["progress"] = progress

    weights = calculate_weights(words)
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


def calculate_weights(words):
    """Расчёт весов слов по ошибкам"""

    weights = []

    for word in words:
        total = word.correct_answers + word.wrong_answers

        if total == 0:
            error_rate = 0
        else:
            error_rate = word.wrong_answers / total

        weight = 1

        if error_rate > 0.3:
            weight += error_rate * 5

        weights.append(weight)

    return weights


def process_answer(request, word):
    """Проверка ответа пользователя"""

    user_answer = request.POST.get("answer", "")
    wrong_translation = word.russian

    if user_answer.strip().lower() == word.russian.strip().lower():
        result = "correct"
        word.correct_answers += 1
    else:
        result = "wrong"
        word.wrong_answers += 1

    word.save()

    return result, wrong_translation


def reset_train(request):
    """Сброс прогресса тренировки"""
    request.session["progress"] = 0
    return redirect("train")


def stats(request):
    """Статистика слов"""

    words = Word.objects.all()

    data = []

    for w in words:
        total = w.correct_answers + w.wrong_answers

        if total > 0:
            percent = round((w.correct_answers / total) * 100)
        else:
            percent = None

        data.append({
            "word": w,
            "correct": w.correct_answers,
            "wrong": w.wrong_answers,
            "percent": percent,
            "is_new": total == 0
        })

    data.sort(key=lambda x: (x["is_new"], -(x["percent"] or 0)))

    return render(request, "trainer/stats.html", {"data": data})


def add_word(request):
    """Добавление нового слова"""

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = WordForm()

    return render(request, "trainer/add.html", {"form": form})