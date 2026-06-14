class TestWorkoutLogs:
    async def test_create_workout_log(self, client, auth_headers, workout):
        """Создание лога тренировки возвращает 201."""
        response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["workout_id"] == workout["id"]
        assert "date" in data
        assert "id" in data
        assert "user_id" in data

    async def test_create_workout_log_unauthorized(self, client, workout):
        """Неавторизованный запрос возвращает 401."""
        response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
        )

        assert response.status_code == 401

    async def test_get_workout_logs_empty(self, client, auth_headers):
        """Список логов пуст для нового пользователя."""
        response = await client.get("/workout-logs/", headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == []

    async def test_get_workout_logs(self, client, auth_headers, workout):
        """Список содержит созданный лог."""
        create_response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
            headers=auth_headers,
        )

        assert create_response.status_code == 201

        response = await client.get("/workout-logs/", headers=auth_headers)

        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_get_workout_log_by_id(self, client, auth_headers, workout):
        """Получение лога по id."""
        create_response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
            headers=auth_headers,
        )

        assert create_response.status_code == 201

        log_id = create_response.json()["id"]

        response = await client.get(f"/workout-logs/{log_id}", headers=auth_headers)

        assert response.status_code == 200
        assert response.json()["id"] == log_id

    async def test_get_workout_log_not_found(self, client, auth_headers):
        """Несуществующий лог возвращает 404."""
        response = await client.get("/workout-logs/999", headers=auth_headers)

        assert response.status_code == 404

    async def test_other_user_cannot_see_log(self, client, auth_headers, workout):
        """Другой пользователь не видит чужой лог."""
        create_response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
            headers=auth_headers,
        )

        assert create_response.status_code == 201

        log_id = create_response.json()["id"]

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

        response = await client.get(f"/workout-logs/{log_id}", headers=other_headers)

        assert response.status_code == 404

        response = await client.get("/workout-logs/", headers=other_headers)

        assert response.status_code == 200
        assert response.json() == []

    async def test_multiple_logs_for_same_workout(self, client, auth_headers, workout):
        """Можно создать несколько логов для одной тренировки."""
        first_response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
            headers=auth_headers,
        )

        second_response = await client.post(
            "/workout-logs/",
            json={
                "workout_id": workout["id"],
            },
            headers=auth_headers,
        )

        assert first_response.status_code == 201
        assert second_response.status_code == 201

        response = await client.get("/workout-logs/", headers=auth_headers)

        assert response.status_code == 200
        assert len(response.json()) == 2
