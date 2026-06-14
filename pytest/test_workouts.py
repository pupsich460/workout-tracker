class TestWorkouts:
    async def test_create_workout(self, client, auth_headers):
        """Создание тренировки возвращает 200 и данные."""
        response = await client.post(
            "/workouts/",
            json={
                "name": "Силовая",
                "description": "Описание",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Силовая"
        assert data["description"] == "Описание"
        assert "id" in data

    async def test_create_workout_without_description(self, client, auth_headers):
        """Создание тренировки без описания — description необязателен."""
        response = await client.post(
            "/workouts/",
            json={
                "name": "Без описания",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Без описания"

    async def test_create_workout_unauthorized(self, client):
        """Неавторизованный запрос возвращает 401."""
        response = await client.post("/workouts/", json={"name": "Тест"})
        assert response.status_code == 401

    async def test_get_workouts_empty(self, client, auth_headers):
        """Список тренировок пуст для нового пользователя."""
        response = await client.get("/workouts/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_workouts(self, client, auth_headers, workout):
        """Список тренировок содержит созданную тренировку."""
        response = await client.get("/workouts/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == workout["id"]

    async def test_get_workout_by_id(self, client, auth_headers, workout):
        """Получение тренировки по id."""
        response = await client.get(f"/workouts/{workout['id']}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == workout["name"]

    async def test_get_workout_not_found(self, client, auth_headers):
        """Несуществующая тренировка возвращает 404."""
        response = await client.get("/workouts/999", headers=auth_headers)
        assert response.status_code == 404

    async def test_update_workout(self, client, auth_headers, workout):
        """PATCH обновляет поля тренировки."""
        response = await client.patch(
            f"/workouts/{workout['id']}",
            json={
                "name": "Обновлённое название",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Обновлённое название"

    async def test_update_workout_not_found(self, client, auth_headers):
        """PATCH несуществующей тренировки возвращает 404."""
        response = await client.patch(
            "/workouts/999", json={"name": "XX"}, headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_workout(self, client, auth_headers, workout):
        """Удаление тренировки возвращает 204."""
        response = await client.delete(
            f"/workouts/{workout['id']}", headers=auth_headers
        )
        assert response.status_code == 204

        get_response = await client.get(
            f"/workouts/{workout['id']}", headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_delete_workout_not_found(self, client, auth_headers):
        """Удаление несуществующей тренировки возвращает 404."""
        response = await client.delete("/workouts/999", headers=auth_headers)
        assert response.status_code == 404

    async def test_other_user_cannot_access_workout(
        self, client, workout, auth_headers
    ):
        """Другой пользователь не видит чужую тренировку."""
        await client.post(
            "/auth/register",
            json={
                "email": "other@example.com",
                "password": "otherpass",
            },
        )
        login = await client.post(
            "/auth/jwt/login",
            data={
                "username": "other@example.com",
                "password": "otherpass",
            },
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.get(f"/workouts/{workout['id']}", headers=other_headers)
        assert response.status_code == 404

    async def test_get_workouts_pagination(self, client, auth_headers):
        """Пагинация — limit и offset работают корректно."""
        for i in range(5):
            await client.post(
                "/workouts/",
                json={"name": f"Тренировка {i}"},
                headers=auth_headers,
            )

        response = await client.get(
            "/workouts/?limit=2&offset=0", headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

        response = await client.get(
            "/workouts/?limit=2&offset=2", headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

        response = await client.get(
            "/workouts/?limit=2&offset=4", headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_other_user_cannot_delete_workout(
        self, client, workout, auth_headers
    ):
        """Другой пользователь не может удалить чужую тренировку."""
        await client.post(
            "/auth/register",
            json={"email": "other3@example.com", "password": "otherpass"},
        )
        login = await client.post(
            "/auth/jwt/login",
            data={"username": "other3@example.com", "password": "otherpass"},
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.delete(
            f"/workouts/{workout['id']}", headers=other_headers
        )
        assert response.status_code == 404

    async def test_other_user_cannot_update_workout(
        self, client, workout, auth_headers
    ):
        """Другой пользователь не может обновить чужую тренировку."""
        await client.post(
            "/auth/register",
            json={"email": "other4@example.com", "password": "otherpass"},
        )
        login = await client.post(
            "/auth/jwt/login",
            data={"username": "other4@example.com", "password": "otherpass"},
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.patch(
            f"/workouts/{workout['id']}",
            json={"name": "Взломано"},
            headers=other_headers,
        )
        assert response.status_code == 404


class TestWorkoutExercises:
    async def test_add_exercise_to_workout(
        self, client, auth_headers, workout, exercise
    ):
        """Добавление упражнения в тренировку возвращает 201."""
        response = await client.post(
            f"/workouts/{workout['id']}/exercises",
            json={
                "workout_id": workout["id"],
                "exercise_id": exercise["id"],
                "sets": 3,
                "reps": 10,
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["sets"] == 3
        assert data["reps"] == 10
        assert data["exercise"]["id"] == exercise["id"]

    async def test_add_exercise_to_nonexistent_workout(
        self, client, auth_headers, exercise
    ):
        """Добавление упражнения в несуществующую тренировку возвращает 404."""
        response = await client.post(
            "/workouts/999/exercises",
            json={
                "workout_id": 999,
                "exercise_id": exercise["id"],
                "sets": 3,
                "reps": 10,
            },
            headers=auth_headers,
        )
        assert response.status_code == 404

    async def test_get_workout_exercises(self, client, auth_headers, workout, exercise):
        """Получение списка упражнений тренировки."""
        await client.post(
            f"/workouts/{workout['id']}/exercises",
            json={
                "workout_id": workout["id"],
                "exercise_id": exercise["id"],
                "sets": 3,
                "reps": 10,
            },
            headers=auth_headers,
        )

        response = await client.get(
            f"/workouts/{workout['id']}/exercises", headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_get_exercises_of_empty_workout(self, client, auth_headers, workout):
        """Список упражнений пустой тренировки — пустой список."""
        response = await client.get(
            f"/workouts/{workout['id']}/exercises", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_add_duplicate_exercise_to_workout(
        self, client, auth_headers, workout, exercise
    ):
        """Добавление одного и того же упражнения дважды возвращает 400."""
        await client.post(
            f"/workouts/{workout['id']}/exercises",
            json={
                "workout_id": workout["id"],
                "exercise_id": exercise["id"],
                "sets": 3,
                "reps": 10,
            },
            headers=auth_headers,
        )

        response = await client.post(
            f"/workouts/{workout['id']}/exercises",
            json={
                "workout_id": workout["id"],
                "exercise_id": exercise["id"],
                "sets": 4,
                "reps": 8,
            },
            headers=auth_headers,
        )
        assert response.status_code == 400

    async def test_delete_exercise_from_workout(
        self, client, auth_headers, workout, exercise
    ):
        """Удаление упражнения из тренировки возвращает 204."""
        await client.post(
            f"/workouts/{workout['id']}/exercises",
            json={
                "workout_id": workout["id"],
                "exercise_id": exercise["id"],
                "sets": 3,
                "reps": 10,
            },
            headers=auth_headers,
        )

        response = await client.delete(
            f"/workouts/{workout['id']}/exercises/{exercise['id']}",
            headers=auth_headers,
        )
        assert response.status_code == 204

        get_response = await client.get(
            f"/workouts/{workout['id']}/exercises", headers=auth_headers
        )
        assert get_response.json() == []

    async def test_delete_nonexistent_exercise_from_workout(
        self, client, auth_headers, workout
    ):
        """Удаление несуществующего упражнения из тренировки возвращает 404."""
        response = await client.delete(
            f"/workouts/{workout['id']}/exercises/999",
            headers=auth_headers,
        )
        assert response.status_code == 404

    async def test_add_nonexistent_exercise_to_workout(
        self, client, auth_headers, workout
    ):
        """Добавление несуществующего упражнения возвращает 404."""
        response = await client.post(
            f"/workouts/{workout['id']}/exercises",
            json={
                "workout_id": workout["id"],
                "exercise_id": 999,
                "sets": 3,
                "reps": 10,
            },
            headers=auth_headers,
        )
        assert response.status_code == 404
