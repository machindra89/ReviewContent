SELECT DISTINCT prj.pkey AS project_key, rslg.slug AS repository_slug
FROM project prj
JOIN repository r ON r.project_id = prj.id
JOIN repository_config rc ON rc.repository_id = r.id
JOIN repository_settings rs ON rs.repository_id = r.id
JOIN repository_settings_merge_check rsmc ON rsmc.repository_settings_id = rs.id
JOIN repository_slug rslg ON rslg.repository_id = r.id
WHERE rsmc.enabled = true
ORDER BY project_key ASC, repository_slug ASC;


